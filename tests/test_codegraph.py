from pathlib import Path
import unittest

from codegraph.Codegraph.core import build_index


class TestCodeGraph(unittest.TestCase):

    def test_build_index(self):
        index = build_index("codegraph/Codegraph")
        self.assertIsNotNone(index)


if __name__ == "__main__":
    unittest.main()
    