"""Unit tests: Tests the utility functions"""

# Python imports
import json
import unittest

# 3rd party imports
from anytree import Node
from anytree.exporter import DictExporter

# Local imports
# from sfs.utils import build_tree_from_files


class TestUtils(unittest.TestCase):
    """Unit tests: Checks the tree construction that is used for the synthetic file structure"""

    def setUp(self) -> None:
        self.exporter = DictExporter()

    def test_empty_tree_build(self) -> None:
        tree = build_tree_from_files([])
        d_tree = self.exporter.export(tree)
        d_root_node = self.exporter.export(Node("Root"))
        self.assertCountEqual(d_tree, d_root_node)

    def test_simple_build_tree(self) -> None:
        with open('./tests/unit/test_data.json', 'r') as f:
            test_object_list = json.load(f)
        test_obj = test_object_list['test_obj1']
        input = test_obj[0]
        expected_output = test_obj[1]

        tree = build_tree_from_files(input)
        actual = self.exporter.export(tree)
        self.assertCountEqual(actual, expected_output)
