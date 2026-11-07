"""Run repository delivery checks and retain process/test evidence for this revision."""
from datetime import datetime, timezone
import json
import subprocess
import sys
import unittest

from publish_parent_plate_access import R, W, write


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    original = subprocess.Popen
    children = []
    receipts = []

    class Tracked(original):
        # Keep Popen a class: asyncio.windows_utils subclasses it on Windows.
        def __init__(self, *args, **kwargs):
            kwargs['creationflags'] = kwargs.get('creationflags', 0) | 0x08004000
            super().__init__(*args, **kwargs)
            record = dict(pid=self.pid, start_utc=now(), command=args[0] if args else kwargs.get('args'),
                          owner='parent_plate_access_20261027', purpose='repository verification')
            children.append((self, record))
            receipts.append(record)
            write(W/'delivery_check_processes.json', receipts)

    subprocess.Popen = Tracked
    results = {}
    try:
        for label, arguments in [
            ('print_set', ['tools/assembly_parts.py', 'check', 'parent_hand_service']),
            ('all_print_sets', ['tools/assembly_parts.py', 'check']),
            ('tidy', ['tools/tidy_workspace.py', 'check']),
        ]:
            completed = subprocess.run([sys.executable, *arguments], cwd=R, capture_output=True,
                                       encoding='utf-8', errors='replace', timeout=120)
            log = W/(label+'_check.log')
            log.write_text(completed.stdout+completed.stderr, encoding='utf-8')
            results[label] = dict(passed=completed.returncode == 0, exit_code=completed.returncode,
                                  log=log.relative_to(R).as_posix())
            print(label, completed.returncode, flush=True)

        screening = {}
        (W/'overhang').mkdir(exist_ok=True)
        for name in ['floor_plate', 'sony_mount_plate', 'sony_fixed_column_0',
                     'gnss_sony_shared_column', 'battery_base', 'ann_mb1_coax_ring_service']:
            output = W/'overhang'/(name+'.json')
            command = [sys.executable, '-m', 'topopt', 'overhang',
                       str(R/'assemblies/parent_hand_service/parts'/(name+'.stl')),
                       '--angle', '45', '--axis', 'Z', '--json', str(output)]
            completed = subprocess.run(command, cwd=R, capture_output=True,
                                       encoding='utf-8', errors='replace', timeout=60)
            (W/'overhang'/(name+'.log')).write_text(completed.stdout+completed.stderr, encoding='utf-8')
            screening[name] = dict(exit_code=completed.returncode,
                                   result=json.loads(output.read_text(encoding='utf-8')) if output.exists() else None)
        results['overhang_screening'] = dict(parts=screening, note='Area screening only; bridges and physical printing require separate review.')

        # Same discovery as: python -m unittest discover -s tools/tests.
        with (W/'unittest.log').open('w', encoding='utf-8') as log:
            suite = unittest.defaultTestLoader.discover(str(R/'tools/tests'))
            result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
        results['unittest'] = dict(passed=result.wasSuccessful(), tests_run=result.testsRun,
                                  failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
                                  log=(W/'unittest.log').relative_to(R).as_posix(),
                                  problems=[dict(test=str(test), traceback=detail)
                                            for test, detail in result.failures+result.errors])
        print('unittest', result.testsRun, 'failures', len(result.failures), 'errors', len(result.errors), flush=True)
    finally:
        subprocess.Popen = original
        for child, record in children:
            if child.poll() is None:
                # Only handles returned by this wrapper may be stopped.
                child.terminate()
                try:
                    child.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait(timeout=10)
                record['cleanup_terminated'] = True
            record.update(exit_code=child.poll(), ended_utc=now())
        write(W/'delivery_check_processes.json', receipts)
        write(W/'delivery_checks.json', dict(checked_utc=now(), checks=results,
                                            task_children_exited=all(p.poll() is not None for p, _ in children)))


if __name__ == '__main__':
    main()
