# build.ps1 — 部品/アセンブリのビルド (PowerShell 5.1)
#
#   .\build.ps1                                                   # printed 部品を全部
#   .\build.ps1 parts\child\interior\printed\child_tray_deck      # 個別(フォルダ指定)
#   .\build.ps1 -Assemblies                                       # アセンブリを全部
#   .\build.ps1 -Assemblies assemblies\child_assembly             # アセンブリ個別
#   .\build.ps1 -NoStep                                           # STL+PNG だけ(高速)
#
# 部品の入出力は同じフォルダ:
#   parts\...\<name>\<name>.scad -> <name>.stl / <name>.step / _work/images/<name>_preview.png
# バリアント(同じ .scad から寸法違いを出す)は同フォルダの variants.txt を参照。
param(
    [string[]]$Paths,
    [switch]$Assemblies,
    [switch]$NoStep,
    [switch]$NoPreview,
    [switch]$NoVerify      # アセンブリ STEP の配置検証 (verify_asm_step.py, 1〜2分) を飛ばす
)

$env:PYTHONIOENCODING = "utf-8"   # inspect_mesh.py の Unicode 出力を cp932 で落とさない

$Root = if ($PSScriptRoot) { $PSScriptRoot } elseif ($MyInvocation.MyCommand.Path) { Split-Path -Parent $MyInvocation.MyCommand.Path } else { (Get-Location).Path }
$Oscad   = "C:\Program Files\OpenSCAD\openscad.exe"
$FreeCad = "C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe"
$Inspect = "C:\Users\ryupc\.claude\skills\3d-print-design\scripts\inspect_mesh.py"
$Conv    = Join-Path $Root "scad\lib\csg_to_step.py"
$MeshConv= Join-Path $Root "scad\lib\stl_to_step.py"
$AsmGen  = Join-Path $Root "scad\lib\asm_gen.py"
$AsmStep = Join-Path $Root "scad\lib\asm_to_step.py"
$AsmStl  = Join-Path $Root "scad\lib\asm_to_stl.py"
$AsmVerify = Join-Path $Root "scad\lib\verify_asm_step.py"
$PrintSync = Join-Path $Root "tools\assembly_parts.py"
$Tidy = Join-Path $Root "tools\tidy_workspace.py"

# アセンブリ プレビューのカメラ (--camera=tx,ty,tz,rx,ry,rz,dist / --viewall で dist 自動)
$AsmViews = @(
    @{ Name = "iso";   Cam = "--camera=0,0,0,60,0,25,0"  },
    @{ Name = "front"; Cam = "--camera=0,0,0,90,0,0,0"   },
    @{ Name = "side";  Cam = "--camera=0,0,0,90,0,90,0"  },
    @{ Name = "top";   Cam = "--camera=0,0,0,0,0,0,0"    }
)

function Rel($p) { return $p.Replace($Root, "").TrimStart("\") }

# openscad.exe は GUI サブシステムのバイナリなので、`& $Oscad ...` では
# PowerShell が終了を待たずに次の行へ進んでしまう。待たずに進むと STL を
# 書き終える前に inspect_mesh.py が走り、「ファイルが無い」か**前回の
# 古い STL を測る**(=直した形状が反映されていないのに OK に見える)。
# Start-Process -Wait で必ず終了を待つこと。
function Invoke-Oscad([string[]]$argList) {
    # Codex/一部IDEは Path と PATH を同時に注入することがあり、Windows PowerShell
    # 5.1 の Start-Process は環境辞書の重複キーで失敗する。.NET Processをシェル
    # 実行すれば同じ環境でも衝突せず、GUIサブシステムの終了を確実に待てる。
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $Oscad
    $psi.Arguments = ($argList -join " ")
    $psi.UseShellExecute = $true
    $proc = [System.Diagnostics.Process]::Start($psi)
    $proc.WaitForExit()
    if ($proc.ExitCode -ne 0) { throw "OpenSCAD failed: exit $($proc.ExitCode)" }
}
function Q($p) { return '"' + $p + '"' }

# variants.txt: 1行1バリアント "<接尾辞> <var=値> <var=値> ..."  ('#' 始まりはコメント)
#   例)  child   tilt_deg=0
#        parent  tilt_deg=20
function Get-Variants($dir) {
    $f = Join-Path $dir "variants.txt"
    if (-not (Test-Path $f)) { return @(@{ Suffix = ""; Defs = @() }) }
    $list = @()
    foreach ($line in (Get-Content $f)) {
        $t = $line.Trim()
        if ($t -eq "" -or $t.StartsWith("#")) { continue }
        $tok = @($t -split "\s+")
        $defs = @()
        if ($tok.Count -gt 1) {
            foreach ($d in $tok[1..($tok.Count - 1)]) { $defs += "-D"; $defs += ($d -replace '"', '\"') }
        }
        $list += @{ Suffix = $tok[0]; Defs = $defs }
    }
    if ($list.Count -eq 0) { return @(@{ Suffix = ""; Defs = @() }) }
    return $list
}

function Build-Part($scad) {
    if (-not (Test-Path $scad)) { Write-Host "!! not found: $scad" -ForegroundColor Red; return }
    $file = Get-Item $scad
    $dir  = $file.Directory.FullName
    $name = $file.BaseName
    $stlFormatArgs = @()
    $stepCoplanar = $false
    $manufacturingPath = Join-Path $dir "manufacturing.json"
    if (Test-Path -LiteralPath $manufacturingPath) {
        $manufacturing = Get-Content -LiteralPath $manufacturingPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $stepCoplanar = ($manufacturing.step_coplanar_merge -eq $true)
        if ($manufacturing.stl_export_format) {
            if ($manufacturing.stl_export_format -notin @("asciistl", "binstl")) { throw "Invalid stl_export_format" }
            $stlFormatArgs = @("--export-format", $manufacturing.stl_export_format)
        }
    }
    foreach ($v in (Get-Variants $dir)) {
        $out  = if ($v.Suffix) { "$($name)_$($v.Suffix)" } else { $name }
        $stl  = Join-Path $dir "$out.stl"
        $work = Join-Path $dir "_work"
        $images = Join-Path $work "images"
        $intermediate = Join-Path $work "intermediate"
        New-Item -ItemType Directory -Force -Path $images,$intermediate | Out-Null
        $csg  = Join-Path $intermediate "$out.csg"
        $step = Join-Path $dir "$out.step"
        Write-Host "### $out" -ForegroundColor Cyan

        Invoke-Oscad (@() + $v.Defs + $stlFormatArgs + @("-o", (Q $stl), (Q $file.FullName)))
        python (Join-Path $Root "tools/clean_stl_degenerates.py") $stl --configured --report (Join-Path $work "analysis/$out-degeneracy.json")
        if ($LASTEXITCODE -ne 0) { throw "STL degeneracy cleanup failed" }
        if (-not $NoStep) {
            if ($stepCoplanar) {
                $stepMesh = Join-Path $intermediate "$out-step-mesh.stl"
                python (Join-Path $Root "tools/compact_coplanar_mesh.py") $stl --out $stepMesh --report (Join-Path $work "analysis/$out-step-coplanar.json")
                if ($LASTEXITCODE -ne 0) { throw "Coplanar STEP input failed" }
                $env:STL_IN = $stepMesh; $env:STEP_OUT = $step
                & $FreeCad $MeshConv
                if ($LASTEXITCODE -ne 0) { throw "Compact STEP conversion failed" }
            } else {
            Invoke-Oscad (@() + $v.Defs + @("-o", (Q $csg), (Q $file.FullName)))
            $csgStamp = (Get-Item $csg).LastWriteTimeUtc
            $env:OPENSCAD = $Oscad; $env:CSG_IN = $csg; $env:STEP_OUT = $step; $env:STL_REF = $stl
            & $FreeCad $Conv
            # FreeCADのOpenSCAD importerは2D hullでDXF addonを要求する場合がある。
            # また hull()/teardrop を含む部品では「書けたが形が違う」STEP が出ることがある
            # (csg_to_step.py が STL_REF と体積/外形を突き合わせ、違えば STEP を書かない)。
            # STEPが更新されなければ、検証済みSTLからfaceted STEPへ確実にフォールバック。
            $needFallback = (-not (Test-Path $step)) -or ((Get-Item $step).LastWriteTimeUtc -lt $csgStamp)
            if ($needFallback) {
                Write-Host "  (CSG->STEP failed; using verified STL fallback)" -ForegroundColor Yellow
                $env:STL_IN = $stl; $env:STEP_OUT = $step
                & $FreeCad $MeshConv
            }
            Remove-Item $csg -ErrorAction SilentlyContinue
            }
        }
        # inspect_mesh.py は <stl>_preview.png を同じ場所に書き、寸法/水密性も出す
        $inspectArgs = @($Inspect, $stl)
        if ($NoPreview) { $inspectArgs += "--no-preview" }
        try { python $inspectArgs | Select-String "Bounding|Watertight" } catch { Write-Host "  (inspect skipped)" }
        $preview = Join-Path $dir "$($out)_preview.png"
        if (Test-Path -LiteralPath $preview) { Move-Item -LiteralPath $preview -Destination (Join-Path $images "$($out)_preview.png") -Force }
        Write-Host "  -> $(Rel $dir)\$out.{stl,step} + _work\images\$($out)_preview.png`n"
    }
}

function Build-Assembly($dir) {
    $name = Split-Path -Leaf $dir
    $json = Join-Path $dir "placement.json"
    $view = Join-Path $dir "$($name)_view.scad"
    $stl  = Join-Path $dir "$name.stl"
    $step = Join-Path $dir "$name.step"
    $images = Join-Path $dir "_work\images"
    New-Item -ItemType Directory -Force -Path $images | Out-Null
    if (-not (Test-Path $json)) { Write-Host "-- skip: $(Rel $dir) (placement.json 未作成)" -ForegroundColor Yellow; return }
    Write-Host "### $name (assembly)" -ForegroundColor Cyan

    python $AsmGen $json $view                       # placement.json -> <name>_view.scad
    if ($LASTEXITCODE -ne 0) { Write-Host "!! asm_gen 失敗" -ForegroundColor Red; return }

    # Keep a mesh assembly beside STEP.  Append already-tessellated component
    # meshes instead of asking OpenSCAD/CGAL to re-boolean detailed PCB models.
    $env:ASM_JSON = $json; $env:ASM_ROOT = $Root; $env:STL_OUT = $stl
    Remove-Item Env:ASM_GROUP -ErrorAction SilentlyContinue
    & $FreeCad $AsmStl
    if ($LASTEXITCODE -ne 0) { throw "assembly STL export failed" }
    # Match the ASCII group key directly. Windows PowerShell 5.1 otherwise
    # decodes UTF-8-without-BOM JSON notes as ANSI before ConvertFrom-Json.
    $hasInterior = Select-String -LiteralPath $json -Pattern '"interior"\s*:' -Quiet
    if ($hasInterior) {
        $interiorStl = Join-Path $dir "$($name)_interior.stl"
        $env:ASM_GROUP = "interior"; $env:STL_OUT = $interiorStl
        & $FreeCad $AsmStl
        if ($LASTEXITCODE -ne 0) { throw "interior assembly STL export failed" }
        Remove-Item Env:ASM_GROUP -ErrorAction SilentlyContinue
    }

    if (-not $NoPreview) {
        foreach ($v in $AsmViews) {
            $png = Join-Path $images "$($name)_$($v.Name).png"
            Invoke-Oscad @("-o", (Q $png), "--imgsize=1400,1050", $v.Cam,
                           "--viewall", "--autocenter", "--colorscheme=Tomorrow", (Q $view))
        }
    }
    if (-not $NoStep) {
        Remove-Item Env:ASM_GROUP -ErrorAction SilentlyContinue
        $env:ASM_JSON = $json; $env:ASM_ROOT = $Root; $env:STEP_OUT = $step
        & $FreeCad $AsmStep
        # STEP を読み戻して各部品が placement.json の位置にあるか確認する。
        # プレビュー PNG は STL、STEP は部品 STEP を合成するので、部品の STEP と STL の
        # 原点が違うと STEP だけ黙ってずれる (2026-09-02 WTE4 ベンダ STEP で発生)。
        if (-not $NoVerify) {
            $env:STEP_IN = $step
            & $FreeCad $AsmVerify 2>&1 | Select-String "verify-asm\]" | Where-Object { $_ -notmatch " ok " }
        }
    }
    Write-Host "  -> $(Rel $dir)\$name.{stl,step} + プレビュー4面`n"
}

# ---- 対象の解決 ---------------------------------------------------------
function Resolve-Dir($p) {
    if ([IO.Path]::IsPathRooted($p)) { return $p.TrimEnd("\") }
    return (Join-Path $Root $p).TrimEnd("\")
}

if ($Assemblies) {
    $targets = if ($Paths) { $Paths | ForEach-Object { Resolve-Dir $_ } }
               else { Get-ChildItem (Join-Path $Root "assemblies") -Directory | ForEach-Object { $_.FullName } }
    foreach ($t in $targets) {
        Build-Assembly $t
        python $PrintSync sync (Split-Path -Leaf $t)
        if ($LASTEXITCODE -ne 0) { throw "print set sync failed" }
    }
    python $Tidy apply
    if ($LASTEXITCODE -ne 0) { throw "workspace tidy failed" }
    exit 0
}

if ($Paths) {
    foreach ($p in $Paths) {
        $t = Resolve-Dir $p
        if (Test-Path $t -PathType Container) { Build-Part (Join-Path $t "$(Split-Path -Leaf $t).scad") }
        else { Build-Part $t }
    }
} else {
    # 規約: 部品フォルダ名 == .scad ファイル名。これに一致するものだけをビルド対象にする。
    Get-ChildItem (Join-Path $Root "parts") -Recurse -Filter *.scad -File |
        Where-Object { $_.BaseName -eq $_.Directory.Name } |
        Sort-Object FullName |
        ForEach-Object { Build-Part $_.FullName }
}
python $Tidy apply
if ($LASTEXITCODE -ne 0) { throw "workspace tidy failed" }
python $PrintSync sync
if ($LASTEXITCODE -ne 0) { throw "print set sync failed" }
exit 0
