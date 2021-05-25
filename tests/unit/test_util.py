"""Unit tests: Tests the utility functions"""

# Python imports
import json
import unittest

# 3rd party imports
from anytree import Node
from anytree.exporter import DictExporter

# Local imports
from src.fuse_utils import build_tree_from_files


class TestUtils(unittest.TestCase):
    """Unit tests: Checks the tree construction that is used for the synthetic file structure"""

    def setUp(self) -> None:
        self.exporter = DictExporter()

    def test_empty_tree_build(self) -> None:
        tree = build_tree_from_files([])
        d_tree = self.exporter.export(tree)
        d_root_node = self.exporter.export(Node("Root"))
        self.assertCountEqual(d_tree, d_root_node)

    @unittest.skip("tested the new refactored version against the old on")
    def test_simple_build_tree(self) -> None:
        with open('./tests/unit/test_data.json', 'r') as f:
            test_object_list = json.load(f)
        for test_obj in test_object_list:
            tree = build_tree_from_files(test_obj)
            tree_new = build_tree_from_files(test_obj)
            d_tree = self.exporter.export(tree)
            d_tree_new = self.exporter.export(tree_new)
            self.assertCountEqual(d_tree, d_tree_new)
