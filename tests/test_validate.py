"""Tests for the pack checker. Run: python -m unittest discover tests"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "checker" / "validate.py"
EXAMPLIA = ROOT / "examples" / "examplia"


def run(*args):
    p = subprocess.run([sys.executable, str(CHECKER), *map(str, args)], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


class Case(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.repo = self.tmp / "repo"
        shutil.copytree(EXAMPLIA, self.repo / "pack")

    def edit(self, rel, old, new):
        f = self.repo / rel
        text = f.read_text(encoding="utf-8")
        self.assertIn(old, text)
        f.write_text(text.replace(old, new), encoding="utf-8")


class Authors(Case):
    def test_examplia_passes(self):
        code, out = run(EXAMPLIA)
        self.assertEqual(code, 0, out)

    def test_placeholder_author_fails(self):
        self.edit("pack/pack.yaml", "A. Author", "<Full name>")
        code, out = run(self.repo / "pack")
        self.assertEqual(code, 1)
        self.assertIn("name (full name)", out)

    def test_missing_credential_fails(self):
        self.edit("pack/pack.yaml", "Member, professional accountancy body", "")
        code, out = run(self.repo / "pack")
        self.assertEqual(code, 1)
        self.assertIn("credential", out)

    def test_to_be_completed_membership_fails(self):
        self.edit("pack/pack.yaml", "00000", "to be completed")
        code, out = run(self.repo / "pack")
        self.assertEqual(code, 1)
        self.assertIn("member_no", out)


class Layout(Case):
    def test_correct_layout_passes_and_names_pack(self):
        code, out = run("--repo", self.repo)
        self.assertEqual(code, 0, out)
        self.assertIn("examplia-general", out)

    def test_flat_layout_fails(self):
        for f in (self.repo / "pack").iterdir():
            if f.is_file() and f.suffix == ".yaml":
                shutil.move(f, self.repo / f.name)
        code, out = run("--repo", self.repo)
        self.assertEqual(code, 1)
        self.assertIn("top of the repository", out)

    def test_template_fails_in_repo_mode(self):
        self.edit("pack/pack.yaml", "examplia-general", "<jurisdiction>-<scope>")
        code, out = run("--repo", self.repo)
        self.assertEqual(code, 1)
        self.assertIn("not been started", out)

    def test_missing_pack_folder_fails(self):
        shutil.rmtree(self.repo / "pack")
        code, out = run("--repo", self.repo)
        self.assertEqual(code, 1)

    def test_blank_sample_left_behind_fails(self):
        (self.repo / "pack" / "examples" / "00-template.yaml").write_text("x: 1\n")
        code, out = run("--repo", self.repo)
        self.assertEqual(code, 1)
        self.assertIn("00-template.yaml", out)


class Versions(Case):
    def test_changelog_mismatch_fails(self):
        self.edit("pack/pack.yaml", '  version: 0.1.0', '  version: 0.2.0')
        code, out = run("--repo", self.repo)
        self.assertEqual(code, 1)
        self.assertIn("must match", out)

    def test_tag_matches_passes(self):
        code, out = run("--repo", self.repo, "--tag", "v0.1.0")
        self.assertEqual(code, 0, out)

    def test_tag_mismatch_fails(self):
        code, out = run("--repo", self.repo, "--tag", "v0.1.1")
        self.assertEqual(code, 1)
        self.assertIn("does not match", out)


if __name__ == "__main__":
    unittest.main()
