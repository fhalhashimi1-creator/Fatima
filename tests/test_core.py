import tempfile
import unittest
from pathlib import Path

from codegraph.Codegraph.core import build_index, search, tokens


class CodeGraphCoreTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)

        (root / "login.py").write_text(
            "from validators import check_password\n"
            "def authenticate(user, password):\n"
            "    return check_password(password)\n"
        )

        (root / "validators.py").write_text(
            "def check_password(password):\n"
            "    return len(password) > 8\n"
        )

        (root / "billing.py").write_text(
            "def invoice(amount):\n"
            "    return amount\n"
        )

        self.index = build_index(root)

    def tearDown(self):
        self.temp.cleanup()

    def test_index_count(self):
        self.assertEqual(len(self.index["files"]), 3)

    def test_import_edge_is_bidirectional(self):
        self.assertIn(
            "validators.py",
            self.index["files"]["login.py"]["neighbors"]
        )
        self.assertIn(
            "login.py",
            self.index["files"]["validators.py"]["neighbors"]
        )

    def test_search_finds_login(self):
        self.assertEqual(
            search(self.index, "authenticate login")[0]["file"],
            "login.py"
        )

    def test_irrelevant_query_returns_empty(self):
        self.assertEqual(search(self.index, "zebra elephant"), [])

    def test_snake_case_tokens(self):
        self.assertIn("password", tokens("check_password"))

    def test_limit_validation(self):
        with self.assertRaises(ValueError):
            search(self.index, "login", limit=0)


if __name__ == "__main__":
    unittest.main()