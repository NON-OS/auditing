# SPDX-License-Identifier: Apache-2.0
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import metrics  # noqa: E402
import resolve_targets  # noqa: E402


class Metrics(unittest.TestCase):
    def test_counts(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "kernel").mkdir()
            (root / "kernel" / "a.rs").write_text(
                "// a comment\nfn f() {\n    unsafe { core::arch::asm!(\"nop\"); }\n}\n#[allow(dead_code)]\nfn g() {}\n")
            (root / "kernel" / "boot.S").write_text("nop\n")
            (root / "target").mkdir()
            (root / "target" / "skip.rs").write_text("unsafe {}\n")
            (root / "Cargo.lock").write_text("[[package]]\nname = \"a\"\n[[package]]\nname = \"b\"\n")
            result = metrics.measure(root)
        k = result["directories"]["kernel"]
        self.assertEqual(k["unsafe"], 1)
        self.assertEqual(k["inline_asm"], 1)
        self.assertEqual(k["allows"], 1)
        self.assertEqual(k["rust_lines"], 5)
        self.assertEqual(k["asm_lines"], 1)
        self.assertNotIn("target", result["directories"])
        self.assertEqual(result["cargo_lock_packages"], 2)

    def test_markdown_has_a_total_row(self):
        text = metrics.as_markdown({"directories": {"a": {"rust_lines": 3}}, "cargo_lock_packages": 0})
        self.assertIn("| total |", text)


class ResolveTargets(unittest.TestCase):
    OUT = ("aaaa\trefs/tags/v1\n"
           "bbbb\trefs/tags/v1^{}\n"
           "cccc\trefs/heads/main\n")

    def test_annotated_tag_is_peeled(self):
        self.assertEqual(resolve_targets.parse_ls_remote(self.OUT, "tag", "v1"), "bbbb")

    def test_branch(self):
        self.assertEqual(resolve_targets.parse_ls_remote(self.OUT, "branch", "main"), "cccc")

    def test_missing_ref(self):
        self.assertIsNone(resolve_targets.parse_ls_remote(self.OUT, "tag", "v2"))


if __name__ == "__main__":
    unittest.main()
