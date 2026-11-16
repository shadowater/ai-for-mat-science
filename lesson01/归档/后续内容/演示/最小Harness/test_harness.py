"""Offline checks for execution boundaries; does not simulate model ability."""
import json
import math
from pathlib import Path
import tempfile
import unittest
from harness import Tools


class ExecutionChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.record = self.root / 'sample.json'
        self.record.write_text(json.dumps({'sample_id': 'TEST', 'radius_mm': 3}))
        self.tools = Tools(self.record, self.root, 'report')

    def test_cannot_skip_prerequisites(self):
        for action in ['circle_area', 'write_report', 'finish']:
            with self.assertRaises(ValueError):
                self.tools.dispatch({'action': action})
        self.assertFalse((self.root / 'report.md').exists())

    def test_report_uses_file_and_calculated_value(self):
        original = self.record.read_bytes()
        self.tools.dispatch({'action': 'read_record'})
        result = self.tools.dispatch({'action': 'circle_area'})
        self.assertAlmostEqual(result['area_mm2'], 9 * math.pi)
        self.tools.dispatch({'action': 'write_report'})
        self.assertIn('28.27 mm²', (self.root / 'report.md').read_text())
        self.assertTrue(self.tools.dispatch({'action': 'finish'})['completed'])
        self.assertEqual(original, self.record.read_bytes())

    def test_read_only_rejects_side_effects(self):
        tools = Tools(self.record, self.root, 'read')
        tools.read_record()
        with self.assertRaises(ValueError):
            tools.write_report()
        self.assertTrue(tools.finish()['completed'])
        self.assertFalse((self.root / 'report.md').exists())

    def test_invalid_requests_are_not_executed(self):
        for request in [{'action': 'shell'}, {'action': 'read_record', 'path': '/etc/passwd'}, []]:
            with self.assertRaises(ValueError):
                self.tools.dispatch(request)

    def test_failed_reread_invalidates_previous_state(self):
        self.tools.read_record()
        self.tools.circle_area()
        self.tools.write_report()
        self.record.unlink()
        with self.assertRaises(FileNotFoundError):
            self.tools.read_record()
        with self.assertRaises(ValueError):
            self.tools.finish()

    def test_bad_input_does_not_create_report(self):
        for radius in [-1, True, float('inf'), '3']:
            self.record.write_text(json.dumps({'sample_id': 'TEST', 'radius_mm': radius}))
            with self.assertRaises(ValueError):
                self.tools.read_record()
        self.record.unlink()
        with self.assertRaises(FileNotFoundError):
            self.tools.read_record()
        self.assertFalse((self.root / 'report.md').exists())


if __name__ == '__main__':
    unittest.main()
