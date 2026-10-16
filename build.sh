#!/usr/bin/env bash
# build.sh — 部品/アセンブリのビルド (Git Bash 版, build.ps1 と同じ動作)
#
#   ./build.sh                                                # printed 部品を全部
#   ./build.sh parts/child/interior/printed/child_tray_deck   # 個別(フォルダ指定)
#   ./build.sh --assemblies                                   # アセンブリを全部
#   ./build.sh --no-step                                      # STL+PNG だけ(高速)
#
# 部品の入出力は同じフォルダ:
#   parts/.../<name>/<name>.scad -> <name>.stl / <name>.step / <name>_preview.png
set -u
export PYTHONIOENCODING=utf-8

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SRC_DIR" && pwd -W 2>/dev/null || echo "$SRC_DIR")"

OSCAD="/c/Program Files/OpenSCAD/openscad.exe"
FC="/c/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/freecadcmd.exe"
INSPECT="C:/Users/ryupc/.claude/skills/3d-print-design/scripts/inspect_mesh.py"
CONV="$ROOT/scad/lib/csg_to_step.py"
ASM_GEN="$ROOT/scad/lib/asm_gen.py"
ASM_STEP="$ROOT/scad/lib/asm_to_step.py"
PRINT_SYNC="$ROOT/tools/assembly_parts.py"
TIDY="$ROOT/tools/tidy_workspace.py"

DO_STEP=1; DO_PREVIEW=1; MODE=parts; TARGETS=()
for a in "$@"; do
    case "$a" in
        --assemblies) MODE=assemblies ;;
        --no-step)    DO_STEP=0 ;;
        --no-preview) DO_PREVIEW=0 ;;
        *)            TARGETS+=("$a") ;;
    esac
done

# variants.txt: 1行1バリアント "<接尾辞> <var=値> ..."  ('#' 始まりはコメント)
read_variants() {   # $1=dir  -> 行ごとに "suffix<TAB>-D a=1 -D b=2"
    local f="$1/variants.txt"
    if [ ! -f "$f" ]; then printf '\t\n'; return; fi
    local any=0
    while IFS= read -r line; do
        line="${line%%$'\r'}"
        case "$(echo "$line" | tr -d '[:space:]')" in ''|'#'*) continue ;; esac
        local suffix defs=""
        suffix="$(echo "$line" | awk '{print $1}')"
        for d in $(echo "$line" | cut -d' ' -f2-); do defs="$defs -D $d"; done
        printf '%s\t%s\n' "$suffix" "$defs"; any=1
    done < "$f"
    [ "$any" = 0 ] && printf '\t\n'
}

build_part() {      # $1 = .scad の絶対パス
    local scad="$1"
    [ -f "$scad" ] || { echo "!! not found: $scad"; return; }
    local dir name; dir="$(dirname "$scad")"; name="$(basename "$scad" .scad)"
    local format_args=() format="" step_merge=0
    if [ -f "$dir/manufacturing.json" ]; then
        format=$(python -c 'import json,sys; v=json.load(open(sys.argv[1],encoding="utf-8-sig")).get("stl_export_format",""); assert v in ("","asciistl","binstl"), "Invalid stl_export_format"; print(v)' "$dir/manufacturing.json") || return 1
        [ -z "$format" ] || format_args=(--export-format "$format")
        step_merge=$(python -c 'import json,sys; print(int(json.load(open(sys.argv[1],encoding="utf-8-sig")).get("step_coplanar_merge",False)))' "$dir/manufacturing.json") || return 1
    fi
    while IFS=$'\t' read -r suffix defs; do
        local out="$name"; [ -n "$suffix" ] && out="${name}_${suffix}"
        mkdir -p "$dir/_work/images" "$dir/_work/intermediate"
        local stl="$dir/$out.stl" csg="$dir/_work/intermediate/$out.csg" step="$dir/$out.step"
        echo "### $out"
        "$OSCAD" $defs "${format_args[@]}" -o "$stl" "$scad" 2>&1 | grep -iE "error|warning" || true
        python "$ROOT/tools/clean_stl_degenerates.py" "$stl" --configured --report "$dir/_work/analysis/$out-degeneracy.json" || return 1
        if [ "$DO_STEP" = 1 ]; then
            if [ "$step_merge" = 1 ]; then
                local step_mesh="$dir/_work/intermediate/$out-step-mesh.stl"
                python "$ROOT/tools/compact_coplanar_mesh.py" "$stl" --out "$step_mesh" --report "$dir/_work/analysis/$out-step-coplanar.json" || return 1
                STL_IN="$step_mesh" STEP_OUT="$step" "$FC" "$ROOT/scad/lib/stl_to_step.py" || return 1
            else
            "$OSCAD" $defs -o "$csg" "$scad" 2>&1 | grep -iE "error|warning" || true
            OPENSCAD="$OSCAD" CSG_IN="$csg" STEP_OUT="$step" \
                "$FC" "$CONV" 2>&1 | grep -iE "csg2step|error|traceback" || true
            rm -f "$csg"
            fi
        fi
        local iargs=("$INSPECT" "$stl"); [ "$DO_PREVIEW" = 0 ] && iargs+=(--no-preview)
        python "${iargs[@]}" 2>&1 | grep -iE "Bounding|Watertight" || true
        if [ -f "$dir/${out}_preview.png" ]; then mv -f "$dir/${out}_preview.png" "$dir/_work/images/${out}_preview.png"; fi
        echo "  -> ${dir#$ROOT/}/$out.{stl,step} + _work/images/${out}_preview.png"; echo
    done < <(read_variants "$dir")
}

build_assembly() {  # $1 = アセンブリフォルダ
    local dir="$1" name json view step
    name="$(basename "$dir")"; json="$dir/placement.json"
    view="$dir/${name}_view.scad"; step="$dir/$name.step"
    [ -f "$json" ] || { echo "-- skip: ${dir#$ROOT/} (placement.json 未作成)"; return; }
    echo "### $name (assembly)"
    mkdir -p "$dir/_work/images"
    python "$ASM_GEN" "$json" "$view" || { echo "!! asm_gen 失敗"; return; }
    if [ "$DO_PREVIEW" = 1 ]; then
        for v in "iso:0,0,0,60,0,25,0" "front:0,0,0,90,0,0,0" "side:0,0,0,90,0,90,0" "top:0,0,0,0,0,0,0"; do
            "$OSCAD" -o "$dir/_work/images/${name}_${v%%:*}.png" --imgsize=1400,1050 \
                "--camera=${v#*:}" --viewall --autocenter --colorscheme=Tomorrow "$view" 2>&1 | grep -iE "error" || true
        done
    fi
    if [ "$DO_STEP" = 1 ]; then
        ASM_JSON="$json" ASM_ROOT="$ROOT" STEP_OUT="$step" \
            "$FC" "$ASM_STEP" 2>&1 | grep -iE "asm2step|error|traceback" || true
    fi
    python "$PRINT_SYNC" sync "$name" || return 1
    echo "  -> ${dir#$ROOT/}/$name.step + parts/ + _work/images/"; echo
}

abs() { case "$1" in /*|[A-Za-z]:*) echo "${1%/}" ;; *) echo "$ROOT/${1%/}" ;; esac; }

if [ "$MODE" = assemblies ]; then
    if [ "${#TARGETS[@]}" -gt 0 ]; then
        for t in "${TARGETS[@]}"; do build_assembly "$(abs "$t")"; done
    else
        for d in "$ROOT"/assemblies/*/; do build_assembly "${d%/}"; done
    fi
    python "$TIDY" apply || exit 1
    exit 0
fi

if [ "${#TARGETS[@]}" -gt 0 ]; then
    for t in "${TARGETS[@]}"; do
        p="$(abs "$t")"
        if [ -d "$p" ]; then build_part "$p/$(basename "$p").scad"; else build_part "$p"; fi
    done
else
    # 規約: 部品フォルダ名 == .scad ファイル名
    while IFS= read -r f; do
        [ "$(basename "$f" .scad)" = "$(basename "$(dirname "$f")")" ] && build_part "$f"
    done < <(find "$ROOT/parts" -name '*.scad' | sort)
fi

python "$TIDY" apply || exit 1
python "$PRINT_SYNC" sync || exit 1
