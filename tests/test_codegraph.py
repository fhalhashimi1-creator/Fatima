import unittest
import tempfile

from codegraph.Codegraph.core import build_index


class TestCodeGraph(unittest.TestCase):

    def test_build_index(self):
        index = build_index("codegraph/Codegraph")
        self.assertIsNotNone(index)

    def test_empty_project(self):
        with tempfile.TemporaryDirectory() as folder:
            index = build_index(folder)
            self.assertIsNotNone(index)


if __name__ == "__main__":
    unittest.main()
    