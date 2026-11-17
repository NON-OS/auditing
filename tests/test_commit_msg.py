# SPDX-License-Identifier: Apache-2.0
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import check_commit_msg as cm  # noqa: E402
import leak_guard  # noqa: E402

CREDIT = cm.CREDIT


class CommitMessages(unittest.TestCase):
    def test_plain_message_with_the_credit_line_passes(self):
        self.assertEqual(cm.problems_in("Add the claims register\n\nOne line of body.\n\n" + CREDIT + "\n"), [])

    def test_long_subject_and_full_stop_fail(self):
        self.assertTrue(cm.problems_in("A" * 80 + "\n"))
        self.assertTrue(cm.problems_in("Add a file.\n"))

    def test_other_credit_lines_and_banners_fail(self):
        self.assertTrue(cm.problems_in("Add a file\n\nCo-Authored-By: Someone <a@example.com>\n"))
        banner = "Generated " + "with a tool"
        self.assertTrue(cm.problems_in("Add a file\n\n" + banner + "\n"))

    def test_session_and_chat_identifiers_fail(self):
        sesn = "sesn_" + "017saoCLtg" + "KkVVDxr9wKsF6j"
        self.assertTrue(cm.problems_in("Add a file\n\nfrom " + sesn + "\n"))
        link = "claude.ai/" + "chat/" + "0a1b2c3d-1111"
        self.assertTrue(cm.problems_in("Add a file\n\n" + link + "\n"))

    def test_dash_and_emoji_fail(self):
        self.assertTrue(cm.problems_in("Add a file — now\n"))
        self.assertTrue(cm.problems_in("Add a file \U0001F680\n"))


class IdentifierPatterns(unittest.TestCase):
    def hits(self, text):
        return [l for l, p in leak_guard.PATTERNS if p.search(text)]

    def test_identifiers_are_found(self):
        agent = "agent_" + "01K9UQsTd9rwpYidZnQ8sT53"
        self.assertTrue(self.hits("id " + agent))
        console = "platform.claude.com/" + "workspaces/default/sessions/sesn_abcdef123456"
        self.assertTrue(self.hits(console))
        uuid = "0a1b2c3d-4e5f-6789-abcd-ef0123456789"
        self.assertTrue(self.hits("session " + uuid))
        self.assertTrue(self.hits("origin" + "SessionId: x"))

    def test_ordinary_text_is_not_flagged(self):
        for text in ("a session of the audit", "env_var is set", "file_name_here_with_underscores_only",
                     "the agent reads the code", "release v0.9.3.5"):
            with self.subTest(text=text):
                self.assertEqual(self.hits(text), [])


if __name__ == "__main__":
    unittest.main()
