# SPDX-License-Identifier: Apache-2.0
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import style_check  # noqa: E402


class StyleCheck(unittest.TestCase):
    def test_clean_text_passes(self):
        self.assertEqual(style_check.check_text("The loader checks the signature.\n", "x"), [])

    def test_forbidden_characters_are_found(self):
        for ch in ("—", "–", "…", "“", "’"):
            with self.subTest(ch=ch):
                self.assertTrue(style_check.check_text(f"a {ch} b\n", "x"))

    def test_inflated_words_are_found(self):
        self.assertTrue(style_check.check_text("This is a pivotal result.\n", "x"))
        self.assertTrue(style_check.check_text("We leverage the parser.\n", "x"))

    def test_words_inside_identifiers_are_not_found(self):
        self.assertEqual(style_check.check_text("The function is named leverage_table.\n", "x"), [])

    def test_code_is_exempt(self):
        text = "Before.\n\n```\nthis quotes the word pivotal on purpose\n```\n\nUse `robust` in code.\n"
        self.assertEqual(style_check.check_text(text, "x"), [])

    def test_stock_phrases_are_found(self):
        self.assertTrue(style_check.check_text("It is important to note that this works.\n", "x"))
        self.assertTrue(style_check.check_text("This is not just fast but also small.\n", "x"))


if __name__ == "__main__":
    unittest.main()
