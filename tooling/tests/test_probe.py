import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tooling import probe


class ProbeEvidenceTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.entries = [self.root / 'first.transit', self.root / 'second.transit']
        for entry in self.entries:
            entry.write_text('CREATE TARGET default AS BEGIN END;\n')

    def test_failure_is_not_converted_to_success_and_later_probes_run(self):
        results = [subprocess.CompletedProcess([], 1, 'compiler refusal', ''),
                   subprocess.CompletedProcess([], 0, 'build accepted', '')]
        with patch.object(probe.subprocess, 'run', side_effect=results) as run:
            records, status = probe.collect(self.entries, self.root)
        self.assertEqual(status, 1)
        self.assertEqual(run.call_count, 2)
        self.assertEqual([r['status'] for r in records], ['build_failed', 'compiled'])
        self.assertEqual(records[0]['stdout'], 'compiler refusal')
        self.assertEqual(records[1]['runtime_tests'], 'not_run')
        self.assertIn('--check', records[0]['command'])

    def test_crashes_timeouts_and_missing_binary_fail(self):
        for result in (subprocess.CompletedProcess([], -11, '', 'crash'),
                       subprocess.TimeoutExpired(['transit'], 60),
                       FileNotFoundError('transit')):
            with self.subTest(result=result):
                arguments = {'side_effect': result} if isinstance(result, Exception) else {'return_value': result}
                with patch.object(probe.subprocess, 'run', **arguments):
                    records, status = probe.collect(self.entries[:1], self.root)
                self.assertEqual(status, 1)
                self.assertNotEqual(records[0]['status'], 'compiled')
                self.assertEqual(records[0]['provider_verification'], 'not_run')

    def test_empty_suite_is_not_success(self):
        self.assertEqual(probe.collect([], self.root), ([], 1))

    def test_compilation_success_does_not_claim_runtime_execution(self):
        with patch.object(probe.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')):
            records, status = probe.collect(self.entries, self.root)
        self.assertEqual(status, 0)
        self.assertTrue(all(r['runtime_tests'] == 'not_run' for r in records))
        self.assertTrue(all(len(next(iter(r['sources'].values()))) == 64 for r in records))


if __name__ == '__main__':
    unittest.main()
