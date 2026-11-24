"""Local, offline integration tests for the baseline tool."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "prepare_target.py"


class TargetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.source = self.base / "fixture-repo"
        self.source.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.source)], check=True)
        subprocess.run(["git", "-C", str(self.source), "config", "user.name", "Fixture"], check=True)
        subprocess.run(["git", "-C", str(self.source), "config", "user.email", "fixture@example.invalid"], check=True)
        (self.source / "README.md").write_text("# Fixture\n", encoding="utf-8")
        (self.source / "LICENSE").write_text("Test license only\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.source), "add", "README.md", "LICENSE"], check=True)
        subprocess.run(["git", "-C", str(self.source), "commit", "-qm", "initial"], check=True)
        self.sha = subprocess.check_output(["git", "-C", str(self.source), "rev-parse", "HEAD"], text=True).strip()
        self.output = self.base / "studies"

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, source, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(source), "--studies", str(self.output), *args],
                              capture_output=True, text=True, encoding="utf-8", errors="replace",
                              env=dict(os.environ, GIT_TERMINAL_PROMPT="0"))

    def test_clone_pin_manifest_and_preserve_existing(self):
        first = self.run_tool(self.source, "--allow-local")
        self.assertEqual(first.returncode, 0, first.stderr)
        study = self.output / f"fixture-repo-{self.sha[:12]}"
        self.assertFalse((study / ".incomplete").exists())
        manifest = (study / "context" / "target-manifest.md").read_text(encoding="utf-8")
        self.assertIn(self.sha, manifest)
        self.assertIn("`main`", manifest)
        self.assertIn("LICENSE", manifest)
        self.assertEqual(subprocess.check_output(["git", "-C", str(study / "target-repo"), "rev-parse", "HEAD"], text=True).strip(), self.sha)
        sentinel = study / "sentinel.txt"
        sentinel.write_text("keep", encoding="utf-8")
        second = self.run_tool(self.source, "--allow-local")
        self.assertEqual(second.returncode, 2)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
        self.assertEqual(list(self.output.glob(".target-*")), [])

    def test_local_paths_require_explicit_fixture_flag(self):
        result = self.run_tool(self.source)
        self.assertEqual(result.returncode, 2)
        self.assertIn("credential-free HTTPS", result.stderr)

    def test_secret_in_url_is_rejected_without_echo(self):
        secret = "SUPER_SECRET_TOKEN_987"
        for url in (f"https://user:{secret}@example.invalid/project.git", f"https://example.invalid/project.git?token={secret}", f"https://[{secret}/project", f"https://example.invalid/{secret}%XX"):
            result = self.run_tool(url)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn(secret, result.stdout + result.stderr)
            self.assertFalse(self.output.exists())

    def test_bad_git_source_is_cleaned(self):
        empty = self.base / "not-repository"
        empty.mkdir()
        result = self.run_tool(empty, "--allow-local")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(list(self.output.glob(".target-*")), [])

    def test_previous_interrupted_temporary_directory_is_not_reused_or_deleted(self):
        self.output.mkdir()
        stale = self.output / ".target-previous-interrupted"
        stale.mkdir()
        (stale / "sentinel.txt").write_text("keep", encoding="utf-8")
        result = self.run_tool(self.source, "--allow-local")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((stale / "sentinel.txt").read_text(encoding="utf-8"), "keep")

    def test_existing_incomplete_study_is_not_modified(self):
        study = self.output / f"fixture-repo-{self.sha[:12]}"
        study.mkdir(parents=True)
        (study / ".incomplete").write_text("prior work", encoding="utf-8")
        result = self.run_tool(self.source, "--allow-local")
        self.assertEqual(result.returncode, 2)
        self.assertEqual((study / ".incomplete").read_text(encoding="utf-8"), "prior work")
        self.assertFalse((study / "target-repo").exists())

    def test_concurrent_runs_never_replace_same_study(self):
        args = [sys.executable, str(SCRIPT), str(self.source), "--studies", str(self.output), "--allow-local"]
        runs = [subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                 encoding="utf-8", errors="replace") for _ in range(2)]
        messages = [run.communicate(timeout=60) for run in runs]
        self.assertEqual(sorted(run.returncode for run in runs), [0, 2], messages)
        study = self.output / f"fixture-repo-{self.sha[:12]}"
        self.assertTrue((study / "context" / "target-manifest.md").is_file())
        self.assertFalse((study / ".incomplete").exists())
        self.assertEqual(list(self.output.glob(".target-*")), [])


if __name__ == "__main__":
    unittest.main()
