"""Pure-local regression tests; no models, tokens, public network, or Mac MCP."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "checkpoint.py"


class LocalStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.run_git("init", "-q")
        self.run_git("config", "user.email", "unit@example.invalid")
        self.run_git("config", "user.name", "Local Test")
        (self.root / ".gitignore").write_text(".eli-engine/\n", encoding="utf-8")
        self.run_git("add", ".gitignore")
        self.run_git("commit", "-qm", "baseline")

    def run_git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              capture_output=True, text=True)

    def run_cli(self, *args, status=0):
        p = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.root,
                           capture_output=True, text=True, timeout=10)
        self.assertEqual(p.returncode, status, (p.stdout, p.stderr))
        return p

    def test_full_local_init_note_snapshot_verify(self):
        self.run_cli("init", "--name", "test")
        self.run_cli("note", "--done", "A-D complete", "--next", "Codex dry run")
        self.run_cli("snapshot", "--reason", "first trusted point")
        self.assertIn("VERIFIED", self.run_cli("verify").stdout)
        self.assertEqual(json.loads(self.run_cli("show").stdout)["done"], "A-D complete")

    def test_no_overwrite_and_no_silent_reactivation(self):
        self.run_cli("init", "--name", "test")
        self.run_cli("init", "--name", "test2", status=3)
        self.run_cli("note", "--done", "done", "--next", "none", "--status", "completed")
        self.run_cli("note", "--done", "again", "--next", "oops", status=3)

    def test_state_drift_fail_closed(self):
        self.run_cli("init", "--name", "test")
        self.run_cli("snapshot", "--reason", "baseline")
        self.run_cli("note", "--done", "changed", "--next", "next")
        self.assertIn("state changed", self.run_cli("verify", status=3).stderr)

    def test_git_dirty_and_new_head_fail_closed(self):
        self.run_cli("init", "--name", "test")
        (self.root / "pending.txt").write_text("pending", encoding="utf-8")
        self.assertIn("dirty", self.run_cli("snapshot", "--reason", "bad", status=3).stderr)
        (self.root / "pending.txt").unlink()
        self.run_cli("snapshot", "--reason", "baseline")
        (self.root / "tracked.txt").write_text("changed", encoding="utf-8")
        self.run_git("add", "tracked.txt")
        self.run_git("commit", "-qm", "new commit")
        self.assertIn("HEAD changed", self.run_cli("verify", status=3).stderr)

    def test_invalid_pointer_cannot_traverse(self):
        self.run_cli("init", "--name", "test")
        f = self.root / ".eli-engine" / "state.json"
        obj = json.loads(f.read_text())
        obj["workspace"] = "/wrong/path"
        f.write_text(json.dumps(obj))
        self.assertIn("relocated", self.run_cli("show", status=3).stderr)


if __name__ == "__main__":
    unittest.main()
