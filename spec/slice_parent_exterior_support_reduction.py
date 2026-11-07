"""Keep enabled detection evidence separate from qualified production profiles."""
import sys
from slice_parent_exterior_qr import main,A

# Existing functional cam lips and short bridges are retained. Review both the
# enabled detector and actual no-support toolpaths; never infer safety from OFF.
QUALIFIED=('camera_mount','parent_oneplate_stand',
           'parent_oneplate_camera_qr_female','parent_oneplate_camera_qr_male')

if __name__=='__main__':
    detect='--detect-only' in sys.argv
    if detect:sys.argv.remove('--detect-only')
    raise SystemExit(main('support_reduction',detect_supports=True,
                         output_root=A/'_work/analysis/support_reduction/support_detection' if detect else None,
                         qualified_no_support=() if detect else QUALIFIED))
