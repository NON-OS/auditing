# SPDX-License-Identifier: Apache-2.0
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_citations as cc  # noqa: E402


def tree(files):
    d = tempfile.TemporaryDirectory()
    root = Path(d.name)
    for name, text in files.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return d, root


class Citations(unittest.TestCase):
    def kernel(self):
        d, root = tree({"src/a.rs": "1\n2\n3\n4\n5\n", "src/b.rs": "x\n", "docs/x.md": ""})
        self.addCleanup(d.cleanup)
        return root

    def ours(self, text):
        d, root = tree({"docs/p.md": text})
        self.addCleanup(d.cleanup)
        return root

    def test_good_file_and_line_citations(self):
        k = self.kernel()
        o = self.ours("See `kernel:src/a.rs`, `kernel:src/a.rs:3` and `kernel:src/a.rs:2-5`.\n")
        self.assertEqual(cc.check_ours(k, o), (3, []))

    def test_missing_file_is_found(self):
        total, found = cc.check_ours(self.kernel(), self.ours("`kernel:src/none.rs`\n"))
        self.assertEqual((total, len(found)), (1, 1))
        self.assertEqual(found[0]["why"], "no such file")

    def test_line_outside_the_file_is_found(self):
        total, found = cc.check_ours(self.kernel(), self.ours("`kernel:src/a.rs:6` and `kernel:src/a.rs:4-9`\n"))
        self.assertEqual(len(found), 2)

    def test_backwards_range_is_found(self):
        _, found = cc.check_ours(self.kernel(), self.ours("`kernel:src/a.rs:4-2`\n"))
        self.assertEqual(len(found), 1)

    def test_text_that_is_not_a_citation_is_ignored(self):
        total, found = cc.check_ours(self.kernel(), self.ours("`src/none.rs` and kernel:src/none.rs and `kernel:`\n"))
        self.assertEqual((total, found), (0, []))

    def test_kernel_docs_mode_reports_stale_citations(self):
        d, root = tree({"src/a.rs": "1\n2\n", "docs/x.md": "ok `src/a.rs:2` stale `src/gone.rs` late `src/a.rs:9`\n"})
        self.addCleanup(d.cleanup)
        total, found = cc.check_kernel_docs(root)
        self.assertEqual(total, 3)
        self.assertEqual(len(found), 2)


    def test_directory_citation_resolves_but_not_with_a_line(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            k = Path(d)
            (k / "src" / "arch").mkdir(parents=True)
            self.assertEqual(cc.problems_in("see `kernel:src/arch`", k, cc.OURS, "x.md", {}), [])
            self.assertEqual(len(cc.problems_in("see `kernel:src/arch:3`", k, cc.OURS, "x.md", {})), 1)
            self.assertEqual(len(cc.problems_in("see `kernel:src/missing`", k, cc.OURS, "x.md", {})), 1)

if __name__ == "__main__":
    unittest.main()
