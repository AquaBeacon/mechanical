"""Boundary and side-effect tests for the local FreeCAD service."""
import importlib
import sys
from pathlib import Path
import tempfile
import unittest
from unittest import mock


CAD_DIR = Path(__file__).resolve().parents[1] / "cad_foundation"
sys.path.insert(0, str(CAD_DIR))
service_module = importlib.import_module("service")
CadService = service_module.CadService


class CadServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.service = CadService(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def put(self, relative, data=b"source bytes"):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_workspace_escape_and_unsupported_inspection_format_are_rejected(self):
        self.put("outside.txt")
        with self.assertRaisesRegex(ValueError, "leaves repository"):
            self.service.inspect_document("../outside.txt")
        with self.assertRaisesRegex(ValueError, "unsupported format"):
            self.service.inspect_document("outside.txt")

    def test_native_generator_must_be_in_an_allowed_project_directory(self):
        outside = self.put("misc/generator.py", b"def build(doc, parameters): return []")
        with mock.patch.object(service_module, "run_job") as run_job:
            with self.assertRaisesRegex(ValueError, "generator must be under"):
                self.service.build_native("misc/generator.py")
            run_job.assert_not_called()
        self.assertTrue(outside.is_file())

    def test_parameter_updates_require_finite_numbers_but_unknown_alias_reaches_worker(self):
        source = self.put("models/editable.FCStd")
        with mock.patch.object(service_module, "run_job", return_value={"status": "mocked"}) as run_job:
            result = self.service.edit_parameters("models/editable.FCStd", {"FutureAlias": 12.5})
            self.assertEqual(result["status"], "mocked")
            plan = run_job.call_args.args[1]
            self.assertEqual(plan["updates"], {"FutureAlias": 12.5})
            self.assertEqual(plan["source"], "models/editable.FCStd")
            for value in (float("nan"), float("inf"), True):
                with self.subTest(value=value):
                    with self.assertRaisesRegex(ValueError, "finite numbers"):
                        self.service.edit_parameters("models/editable.FCStd", {"length": value})
            with self.assertRaisesRegex(ValueError, "finite numbers"):
                self.service.edit_parameters("models/editable.FCStd", {"bad-alias": 4})
            self.assertEqual(run_job.call_count, 1)
        self.assertEqual(source.read_bytes(), b"source bytes")

    def test_export_document_does_not_write_source_when_backend_is_mocked(self):
        source = self.put("models/assembly.FCStd", b"original document")
        before = source.read_bytes()
        with mock.patch.object(service_module, "run_job", return_value={"status": "mocked"}) as run_job:
            result = self.service.export_document("models/assembly.FCStd", ["Body"])
        self.assertEqual(result["status"], "mocked")
        self.assertEqual(run_job.call_args.args[1]["object_names"], ["Body"])
        self.assertEqual(source.read_bytes(), before)

    def test_component_limit_rejects_before_starting_backend(self):
        plan = {"missing": [], "component_count": 2}
        with mock.patch.object(service_module, "make_plan", return_value=plan), \
                mock.patch.object(service_module, "run_job") as run_job:
            with self.assertRaisesRegex(ValueError, "component limit"):
                self.service.export_assembly("assemblies/demo", max_components=1)
            run_job.assert_not_called()

    def test_workspace_lock_is_visible_across_service_instances_and_releases(self):
        second = CadService(self.root)
        with self.service._lock():
            with self.assertRaisesRegex(RuntimeError, "busy"):
                with second._lock():
                    self.fail("second service unexpectedly acquired the active lock")
        with second._lock():
            pass

    def test_open_document_launches_exact_gui_arguments_without_batch_backend(self):
        source = self.put("models/view.FCStd")
        install = self.root / "fake-freecad"
        install.mkdir()
        cmd = install / "FreeCADCmd.exe"
        gui = install / "FreeCAD.exe"
        cmd.touch()
        gui.touch()
        process = mock.Mock(pid=4321)
        with mock.patch.object(service_module, "find_freecad", return_value=str(cmd)), \
                mock.patch.object(service_module.subprocess, "Popen", return_value=process) as popen, \
                mock.patch.object(service_module, "run_job") as run_job:
            result = self.service.open_document("models/view.FCStd")
        self.assertEqual(result["status"], "launch_requested")
        self.assertEqual(result["pid"], 4321)
        self.assertEqual(popen.call_args.args[0], [str(gui), str(source.resolve())])
        self.assertIs(popen.call_args.kwargs["stdout"], service_module.subprocess.DEVNULL)
        self.assertIs(popen.call_args.kwargs["stderr"], service_module.subprocess.DEVNULL)
        run_job.assert_not_called()

    def test_report_reader_rejects_path_traversal_run_id(self):
        with self.assertRaisesRegex(ValueError, "invalid run_id"):
            self.service.read_report("../../outside")


if __name__ == "__main__":
    unittest.main()
