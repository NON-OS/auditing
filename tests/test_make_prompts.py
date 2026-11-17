# SPDX-License-Identifier: Apache-2.0
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "routines"))
import make_prompts  # noqa: E402

REF = "a" * 40


class MakePrompts(unittest.TestCase):
    def test_writes_lead_refuter_and_every_workstream(self):
        with tempfile.TemporaryDirectory() as d:
            written = make_prompts.build("owner/private-audit", REF, d)
            self.assertEqual(len(written), 2 + 14)
            for name in written:
                text = (Path(d) / name).read_text(encoding="utf-8")
                self.assertNotIn("{{", text)
                self.assertIn("owner/private-audit", text)
                self.assertIn(REF, text)

    def test_worker_names_its_workstream_and_checklist(self):
        with tempfile.TemporaryDirectory() as d:
            make_prompts.build("owner/private-audit", REF, d)
            text = (Path(d) / "ws03.md").read_text(encoding="utf-8")
            self.assertIn("ws03-syscalls-capabilities.md", text)
            self.assertIn("notes/ws03/", text)

    def test_bad_inputs_are_refused(self):
        with tempfile.TemporaryDirectory() as d:
            for repo, ref in (("noslash", REF), ("owner/r", "main"), ("owner/r", "a" * 39)):
                with self.subTest(repo=repo, ref=ref):
                    with self.assertRaises(ValueError):
                        make_prompts.build(repo, ref, d)

    def test_unfilled_placeholder_is_an_error(self):
        with self.assertRaises(ValueError):
            make_prompts.fill("hello {{NOPE}}", {})


if __name__ == "__main__":
    unittest.main()
