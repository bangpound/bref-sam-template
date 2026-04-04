import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hooks"))

from post_gen_project import _is_process_successful, run_composer_create_project


class TestIsProcessSuccessful(unittest.TestCase):
    def test_returns_true_on_zero_exit(self):
        proc = MagicMock()
        proc.poll.return_value = 0
        self.assertTrue(_is_process_successful(proc))

    def test_returns_false_on_nonzero_exit(self):
        proc = MagicMock()
        proc.poll.return_value = 1
        self.assertFalse(_is_process_successful(proc))

    def test_returns_false_on_negative_exit(self):
        proc = MagicMock()
        proc.poll.return_value = -1
        self.assertFalse(_is_process_successful(proc))


class TestRunComposerCreateProject(unittest.TestCase):
    def _make_mock_proc(self, exit_code):
        mock_proc = MagicMock()
        mock_proc.poll.return_value = exit_code
        mock_proc.__enter__ = lambda s: s
        mock_proc.__exit__ = MagicMock(return_value=False)
        return mock_proc

    def test_returns_true_on_success(self):
        with patch("post_gen_project.subprocess.Popen", return_value=self._make_mock_proc(0)):
            self.assertTrue(run_composer_create_project())

    def test_returns_false_on_failure(self):
        with patch("post_gen_project.subprocess.Popen", return_value=self._make_mock_proc(1)):
            self.assertFalse(run_composer_create_project())

    def test_invokes_composer_create_project_command(self):
        mock_proc = self._make_mock_proc(0)
        with patch("post_gen_project.subprocess.Popen", return_value=mock_proc) as mock_popen:
            run_composer_create_project()
        args = mock_popen.call_args[0][0]
        self.assertIn("composer", args)
        self.assertIn("create-project", args)


if __name__ == "__main__":
    unittest.main()
