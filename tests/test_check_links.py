# SPDX-License-Identifier: Apache-2.0
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_links  # noqa: E402


class CheckLinks(unittest.TestCase):
    def tree(self, files):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        root = Path(d.name)
        for name, text in files.items():
            p = root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        return root

    def test_good_link(self):
        root = self.tree({"a.md": "[b](b.md)\n", "b.md": "x\n"})
        self.assertEqual(check_links.check(root), (1, []))

    def test_broken_link(self):
        root = self.tree({"a.md": "[b](missing.md)\n"})
        count, problems = check_links.check(root)
        self.assertEqual(count, 1)
        self.assertEqual(len(problems), 1)

    def test_external_and_anchor_links_are_skipped(self):
        root = self.tree({"a.md": "[x](https://example.com) [y](#top)\n"})
        self.assertEqual(check_links.check(root), (0, []))

    def test_links_in_code_are_skipped(self):
        root = self.tree({"a.md": "```\n[b](missing.md)\n```\n`[c](missing.md)`\n"})
        self.assertEqual(check_links.check(root), (0, []))

    def test_relative_to_subdirectory(self):
        root = self.tree({"d/a.md": "[up](../b.md)\n", "b.md": "x\n"})
        self.assertEqual(check_links.check(root), (1, []))


if __name__ == "__main__":
    unittest.main()
