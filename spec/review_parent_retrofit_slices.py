"""Review completed slicer artifacts after an exit timeout, without reslicing."""
import datetime, json, zipfile
import slice_parent_retrofit as slicer

def main():
    evidence = {}
    for number in (1, 2):
        folder = slicer.WORK / ('plate_' + str(number))
        files = ['placed.stl', 'seed.3mf', 'blocked.3mf', 'retrofit_plate_' + str(number) + '.3mf', 'result.json']
        evidence[str(number)] = {name: slicer.sha(folder / name) for name in files}
        result = slicer.read(folder / 'result.json')
        assert result['return_code'] == 0
        output = folder / files[3]
        assert output.stat().st_mtime_ns >= (folder / 'blocked.3mf').stat().st_mtime_ns
        with zipfile.ZipFile(output) as archive:
            assert archive.testzip() is None
            assert len(archive.read('Metadata/plate_1.gcode')) > 1000
    def existing(cmd, folder, purpose):
        number = folder.name.split('_')[-1]
        # Recreated inputs must match the exact STL used by the completed slice.
        assert slicer.sha(folder / 'placed.stl') == evidence[number]['placed.stl']
        for name, expected in evidence[number].items():
            assert slicer.sha(folder / name) == expected, name
    slicer.run = existing
    slicer.attach_blocker = lambda *args: None
    slicer.main()  # Full per-member layer, bed bounds and support exclusion checks.
    record = dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  reason='Plate 2 exported successful result and complete 3MF but did not exit within 240 seconds; task-owned process terminated by timeout handler.',
                  evidence=evidence, output_review_passed=True, process_exit_passed=False)
    slicer.write(slicer.WORK / 'timeout_recovery_review.json', record)
    print('Completed artifact review passed; slicer process timeout remains recorded.')

if __name__ == '__main__':
    main()
