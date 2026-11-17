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


if __name__ == "__main__":
    unittest.main()
