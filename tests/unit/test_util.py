"""Unit tests: Tests the utility functions"""

# Python imports
import json
import unittest

# 3rd party imports
from anytree import Node
from anytree.exporter import DictExporter

# Local imports
from sfs.dir_tree import DirectoryTree


class TestUtils(unittest.TestCase):
    """Unit tests: Checks the tree construction that is used for the synthetic file structure"""

    def setUp(self) -> None:
        self.exporter = DictExporter()

    def test_empty_tree_build(self) -> None:
        tree = DirectoryTree()
        tree.build([], "mirror")
        d_tree = self.exporter.export(tree.directory_tree)
        d_root_node = self.exporter.export(Node("Root"))
        self.assertCountEqual(d_tree, d_root_node)

    def test_simple_build_tree(self) -> None:
        with open('./tests/unit/test_data.json', 'r') as f:
            test_object_list = json.load(f)
        test_obj = test_object_list['test_obj1']
        input = test_obj[0]
        expected_output = test_obj[1]

        tree = DirectoryTree()
        tree.build(input, "mirror")
        actual = self.exporter.export(tree.directory_tree)
        self.assertCountEqual(actual, expected_output)
