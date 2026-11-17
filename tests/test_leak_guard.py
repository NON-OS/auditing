# SPDX-License-Identifier: Apache-2.0
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import leak_guard  # noqa: E402


class LeakGuard(unittest.TestCase):
    def tree(self, files):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        root = Path(d.name)
        for name, text in files.items():
            p = root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        return root

    def test_clean_tree_passes(self):
        self.assertEqual(leak_guard.check(self.tree({"a.md": "Nothing to see.\n"})), [])

    def test_private_key_block_is_found(self):
        marker = "-----BEGIN " + "PRIVATE KEY-----"
        self.assertTrue(leak_guard.check(self.tree({"a.txt": marker + "\n"})))

    def test_github_token_is_found(self):
        token = "ghp_" + "a" * 36
        self.assertTrue(leak_guard.check(self.tree({"a.txt": token})))

    def test_public_ip_is_found_and_reserved_ranges_are_not(self):
        public = ".".join(["8", "8", "4", "4"])
        self.assertTrue(leak_guard.check(self.tree({"a.md": f"host {public}\n"})))
        for ok in ("10.0.0.1", "192.168.1.1", "127.0.0.1", "192.0.2.7", "203.0.113.9", "0.9.3.5"):
            with self.subTest(ip=ok):
                self.assertEqual(leak_guard.check(self.tree({"a.md": f"host {ok}\n"})), [])

    def test_allowlisted_ip_passes(self):
        public = ".".join(["8", "8", "4", "4"])
        root = self.tree({"a.md": f"host {public}\n", "scripts/ipv4_allow.txt": public + "\n"})
        self.assertEqual(leak_guard.check(root), [])

    def test_home_path_naming_a_person_is_found(self):
        path = "/" + "Users" + "/" + "someone" + "/code/x"
        self.assertTrue(leak_guard.check(self.tree({"a.md": path + "\n"})))
        self.assertEqual(leak_guard.check(self.tree({"a.md": "/home/runner/work/x\n"})), [])

    def test_key_file_names_are_found(self):
        self.assertTrue(leak_guard.check(self.tree({"signing_key_v1.txt": "x"})))
        self.assertTrue(leak_guard.check(self.tree({"x.pem": "x"})))

    def test_unpublished_finding_path_is_found(self):
        root = self.tree({"findings/notes.md": "x\n", "findings/published/NKA-2026-001.json": "{}"})
        problems = leak_guard.check(root)
        self.assertEqual(len(problems), 1)
        self.assertIn("findings/notes.md", problems[0])

    def test_banned_terms_file_is_applied(self):
        root = self.tree({"a.md": "Visit the Secret Host today.\n", "private/banned.txt": "secret host\n"})
        self.assertTrue(leak_guard.check(root))

    def test_tracked_private_directory_is_found(self):
        root = self.tree({"a.md": "x\n", "private/notes.md": "x\n"})
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "add", "-f", "private/notes.md"], cwd=root, check=True)
        self.assertTrue(any("private/" in p for p in leak_guard.check(root)))

    def test_repository_is_clean(self):
        self.assertEqual(leak_guard.check(REPO), [])


if __name__ == "__main__":
    unittest.main()
