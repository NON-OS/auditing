# SPDX-License-Identifier: Apache-2.0
import copy
import datetime
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import validate_findings as vf  # noqa: E402

# A synthetic finding, used only to exercise the validator. It describes nothing real.
GOOD = {
    "id": "NKA-0000-001",
    "title": "Synthetic finding used by the tests",
    "component": "test",
    "severity": "low",
    "confidence": "confirmed",
    "adversary": "A1",
    "affected": {"release": True, "main": True, "commits": ["0" * 40]},
    "location": "none:1",
    "cvss": "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:N",
    "description": "A synthetic description that is long enough to pass.",
    "impact": "No impact, this is a test.",
    "scenario": ["Step one of the synthetic scenario."],
    "evidence": {"reproduced": True, "steps": ["Run the test."]},
    "remediation": "No change is needed, this is a test.",
    "status": "fixed",
    "fix": {"commit": "1" * 40},
    "dates": {"reported": "2026-01-01", "fixed": "2026-02-01", "published": "2026-03-01"},
}
TODAY = datetime.date(2026, 6, 1)


class ValidateFindings(unittest.TestCase):
    def check(self, doc, name=None):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        root = Path(d.name)
        (root / "findings" / "schema").mkdir(parents=True)
        (root / "findings" / "published").mkdir(parents=True)
        (root / "findings" / "schema" / "finding.schema.json").write_text(
            (REPO / "findings" / "schema" / "finding.schema.json").read_text())
        (root / "findings" / "published" / (name or doc["id"] + ".json")).write_text(json.dumps(doc))
        return vf.check(root, TODAY)

    def test_good_finding_passes(self):
        self.assertEqual(self.check(GOOD), (1, []))

    def test_missing_field_fails(self):
        doc = copy.deepcopy(GOOD)
        del doc["impact"]
        self.assertTrue(self.check(doc)[1])

    def test_bad_enum_fails(self):
        doc = copy.deepcopy(GOOD)
        doc["severity"] = "catastrophic"
        self.assertTrue(self.check(doc)[1])

    def test_file_name_must_match_id(self):
        self.assertTrue(self.check(GOOD, name="NKA-0000-002.json")[1])

    def test_fixed_needs_fix_commit(self):
        doc = copy.deepcopy(GOOD)
        del doc["fix"]
        self.assertTrue(self.check(doc)[1])

    def test_accepted_risk_and_disputed_need_a_reason(self):
        for status in ("accepted-risk", "disputed"):
            with self.subTest(status=status):
                doc = copy.deepcopy(GOOD)
                doc["status"] = status
                del doc["fix"]
                self.assertTrue(self.check(doc)[1])
                doc["reason"] = "The maintainers decided this is within the design."
                self.assertEqual(self.check(doc)[1], [])

    def test_unknown_status_fails(self):
        doc = copy.deepcopy(GOOD)
        doc["status"] = "disclosed-after-window"
        self.assertTrue(self.check(doc)[1])

    def test_future_publication_fails(self):
        doc = copy.deepcopy(GOOD)
        doc["dates"]["published"] = "2026-12-31"
        self.assertTrue(self.check(doc)[1])

    def test_confirmed_needs_reproduction(self):
        doc = copy.deepcopy(GOOD)
        doc["evidence"]["reproduced"] = False
        self.assertTrue(self.check(doc)[1])

    def test_published_before_reported_fails(self):
        doc = copy.deepcopy(GOOD)
        doc["dates"]["published"] = "2025-12-31"
        self.assertTrue(self.check(doc)[1])

    def test_repository_has_no_problems(self):
        count, problems = vf.check(REPO, TODAY)
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
