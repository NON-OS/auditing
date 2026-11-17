# SPDX-License-Identifier: Apache-2.0
import copy
import datetime
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import validate_claims as vc  # noqa: E402

TODAY = datetime.date(2026, 6, 1)
OPEN = {
    "id": "C-001", "category": "privacy", "text": "A synthetic claim.",
    "source": {"kind": "website", "location": "https://example.com/", "retrieved": "2026-01-01"},
    "to_establish": ["A synthetic question."], "verdict": "unverified",
}
DONE = dict(OPEN, verdict="verified", evidence=["a test"], checked_at="0" * 40, reviewed_at="2026-02-01")
del DONE["to_establish"]


class ValidateClaims(unittest.TestCase):
    def errs(self, claim):
        return vc.problems_for(claim, TODAY)

    def test_open_claim_passes(self):
        self.assertEqual(self.errs(OPEN), [])

    def test_open_claim_needs_questions(self):
        c = copy.deepcopy(OPEN)
        c["to_establish"] = []
        self.assertTrue(self.errs(c))

    def test_verified_claim_passes(self):
        self.assertEqual(self.errs(DONE), [])

    def test_verdict_needs_evidence_and_commit(self):
        for key in ("evidence", "checked_at", "reviewed_at"):
            c = copy.deepcopy(DONE)
            del c[key]
            with self.subTest(missing=key):
                self.assertTrue(self.errs(c))

    def test_caveated_verdict_needs_wording_and_caveats(self):
        c = dict(DONE, verdict="verified-with-caveats")
        self.assertTrue(self.errs(c))
        c.update(suggested_wording="More precise.", caveats="Only on an orderly shutdown.")
        self.assertEqual(self.errs(c), [])

    def test_unverifiable_needs_reason(self):
        c = dict(DONE, verdict="unverifiable", suggested_wording="Checkable wording.")
        self.assertTrue(self.errs(c))
        c["reason"] = "No test can settle it."
        self.assertEqual(self.errs(c), [])

    def test_overstated_needs_a_correction_or_the_maintainers_reason(self):
        c = dict(DONE, verdict="overstated", suggested_wording="Precise wording.")
        self.assertTrue(self.errs(c))
        self.assertEqual(self.errs(dict(c, maintainers_reason="Kept on purpose.")), [])
        self.assertEqual(self.errs(dict(c, corrected_in="1" * 40)), [])
        self.assertTrue(self.errs(dict(c, corrected_in="abc")))

    def test_future_review_fails(self):
        self.assertTrue(self.errs(dict(DONE, reviewed_at="2026-12-31")))

    def test_file_source_needs_commit(self):
        c = dict(OPEN, source={"kind": "readme", "location": "README.md"})
        self.assertTrue(self.errs(c))

    def test_the_real_register_is_valid_and_complete(self):
        count, problems = vc.check(REPO, TODAY)
        self.assertEqual(problems, [])
        self.assertGreaterEqual(count, 20)


if __name__ == "__main__":
    unittest.main()
