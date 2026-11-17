# SPDX-License-Identifier: Apache-2.0
import datetime
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import publish_finding as pf  # noqa: E402

TODAY = datetime.date(2026, 12, 2)
HASH = "a" * 40


def draft(**over):
    d = {
        "id": "NKA-2026-001", "title": "A test finding about a capability check",
        "component": "syscall layer", "severity": "low", "confidence": "supported", "adversary": "A1",
        "preconditions": ["a capsule with a valid token"],
        "affected": {"release": True, "main": True, "commits": [HASH]},
        "location": "kernel:src/example.rs:10-20",
        "cvss": "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N",
        "description": "The handler answers for any process, with no check on the caller.",
        "impact": "A capsule can read another capsule's capability bits.",
        "scenario": ["The capsule picks a pid", "It asks the handler for one bit at a time"],
        "evidence": {"reproduced": False, "steps": ["Read the handler and its dispatch path"]},
        "remediation": "Apply the same visibility test the process listing uses.",
        "dates": {"reported": "2026-11-20"},
    }
    d.update(over)
    return d


class Publish(unittest.TestCase):
    def test_fixed_finding_is_built(self):
        doc = pf.build(draft(), "fixed", HASH, "2026-12-01", today=TODAY)
        self.assertEqual(doc["status"], "fixed")
        self.assertEqual(doc["fix"]["commit"], HASH)
        self.assertEqual(doc["dates"]["published"], "2026-12-02")

    def test_fixed_needs_commit_and_date(self):
        with self.assertRaises(pf.Refused):
            pf.build(draft(), "fixed", None, None, today=TODAY)

    def test_accepted_risk_needs_the_reason(self):
        with self.assertRaises(pf.Refused):
            pf.build(draft(), "accepted-risk", today=TODAY)
        doc = pf.build(draft(), "accepted-risk", reason="The maintainers accept this risk for now.", today=TODAY)
        self.assertEqual(doc["status"], "accepted-risk")

    def test_open_finding_cannot_be_forced_through(self):
        d = draft(status="open", fix={"commit": "b" * 40})
        doc = pf.build(d, "disputed", reason="The maintainers dispute the precondition.", today=TODAY)
        self.assertEqual(doc["status"], "disputed")
        self.assertNotIn("fix", doc)

    def test_leaks_are_refused(self):
        token = "ghp_" + "a" * 36
        with self.assertRaises(pf.Refused):
            pf.build(draft(description="The handler leaks " + token + " into the log."), "fixed", HASH, "2026-12-01", today=TODAY)
        sesn = "sesn_" + "01CazuMzWiiokos7mGnD97wS"
        with self.assertRaises(pf.Refused):
            pf.build(draft(impact="Found in " + sesn + " during a run"), "fixed", HASH, "2026-12-01", today=TODAY)
        with self.assertRaises(pf.Refused):
            pf.build(draft(impact="Reachable at " + ".".join(["8", "8", "4", "4"]) + " from outside"), "fixed", HASH, "2026-12-01", today=TODAY)

    def test_schema_violations_are_refused(self):
        with self.assertRaises(pf.Refused):
            pf.build(draft(severity="catastrophic"), "fixed", HASH, "2026-12-01", today=TODAY)
        with self.assertRaises(pf.Refused):
            pf.build(draft(confidence="confirmed"), "fixed", HASH, "2026-12-01", today=TODAY)

    def test_write_refuses_a_second_publication(self):
        doc = pf.build(draft(), "fixed", HASH, "2026-12-01", today=TODAY)
        with tempfile.TemporaryDirectory() as d:
            p = pf.write(doc, d)
            self.assertTrue(p.exists())
            self.assertEqual(json.loads(p.read_text())["id"], "NKA-2026-001")
            with self.assertRaises(pf.Refused):
                pf.write(doc, d)

    def test_commit_message_obeys_the_commit_rules(self):
        import check_commit_msg as cm
        doc = pf.build(draft(), "fixed", HASH, "2026-12-01", today=TODAY)
        self.assertEqual(cm.problems_in(pf.message(doc)), [])
        long = pf.build(draft(title="A very long title " * 6), "fixed", HASH, "2026-12-01", today=TODAY)
        self.assertEqual(cm.problems_in(pf.message(long)), [])

    def test_commit_makes_one_commit(self):
        doc = pf.build(draft(), "fixed", HASH, "2026-12-01", today=TODAY)
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", d], check=True)
            for k, v in (("user.name", "t"), ("user.email", "t@example.com"), ("commit.gpgsign", "false")):
                subprocess.run(["git", "-C", d, "config", k, v], check=True)
            pf.commit(doc, pf.write(doc, d), d)
            n = subprocess.run(["git", "-C", d, "rev-list", "--count", "HEAD"], capture_output=True, text=True).stdout.strip()
            self.assertEqual(n, "1")


    def test_open_finding_is_published_at_confirmation(self):
        doc = pf.build(draft(), "open", today=TODAY)
        self.assertEqual(doc["status"], "open")
        self.assertNotIn("fix", doc)
        self.assertNotIn("reason", doc)
        self.assertEqual(doc["dates"]["published"], "2026-12-02")

    def test_open_finding_cannot_carry_a_fix(self):
        doc = pf.build(draft(), "open", today=TODAY)
        doc["fix"] = {"commit": HASH}
        import validate_findings as vf
        self.assertTrue(vf.policy(doc, TODAY))

    def test_update_marks_an_open_finding_fixed_and_keeps_its_published_date(self):
        opened = pf.build(draft(), "open", today=TODAY)
        later = datetime.date(2026, 12, 20)
        doc = pf.build(opened, "fixed", HASH, "2026-12-19", today=later, update=True)
        self.assertEqual(doc["status"], "fixed")
        self.assertEqual(doc["dates"]["published"], "2026-12-02")
        self.assertEqual(doc["dates"]["updated"], "2026-12-20")
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(pf.Refused):
                pf.write(doc, d, update=True)
            pf.write(opened, d)
            pf.write(doc, d, update=True)
            self.assertEqual(json.loads((Path(d) / "findings" / "published" / "NKA-2026-001.json").read_text())["status"], "fixed")

    def test_writing_rules_are_enforced(self):
        with self.assertRaises(pf.Refused):
            pf.build(draft(description="The handler answers \u2014 for any process, with no caller check."), "open", today=TODAY)

    def test_pages_and_index_are_rendered_and_stay_in_step(self):
        import render_findings as rf
        doc = pf.build(draft(description="See `kernel:src/example.rs:10` where the handler answers any pid."), "open", today=TODAY)
        with tempfile.TemporaryDirectory() as d:
            pf.write(doc, d)
            pub = Path(d) / "findings" / "published"
            self.assertIn("NKA-2026-001", (pub / "README.md").read_text())
            page = (pub / "NKA-2026-001.md").read_text()
            self.assertIn("Open. Published when it was confirmed", page)
            self.assertNotIn("`kernel:", page)
            self.assertEqual(rf.stale(d), [])
            (pub / "NKA-2026-001.md").write_text("changed")
            self.assertEqual(rf.stale(d), ["NKA-2026-001.md"])


if __name__ == "__main__":
    unittest.main()
