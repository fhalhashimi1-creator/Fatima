import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from codegraph.Codegraph.core import build_index
from codegraph.Codegraph.agent import explain
from codegraph.Codegraph.evaluate import evaluate


class AgentEvaluationTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

        (self.root / "login.py").write_text(
            "from validators import check\n"
            "def login(): return check()\n"
        )

        (self.root / "validators.py").write_text(
            "def check(): return True\n"
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_no_model_does_not_pretend_to_infer(self):
        with patch.dict(
            "os.environ",
            {
                "CODEGRAPH_LLM_URL": "",
                "CODEGRAPH_LLM_MODEL": "",
            },
        ):
            result = explain(
                build_index(self.root),
                "login",
                endpoint="",
                model=""
            )

        self.assertFalse(result["model_used"])
        self.assertIsNone(result["explanation"])

    def test_evaluation_reproducible(self):
        tasks = [
            {
                "query": "login",
                "relevant_files": ["login.py"]
            }
        ]

        result = evaluate(self.root, tasks, k=1)

        self.assertEqual(
            result["methods"]["lexical"]["hit_at_k"], 1
        )
        self.assertEqual(
            result["methods"]["graph"]["hit_at_k"], 1
        )

    def test_empty_tasks_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(self.root, [])


if __name__ == "__main__":
    unittest.main()
    