# Python imports
import logging
from typing import List

# 3rd party imports
from anytree import Node, Resolver, RenderTree
from anytree.resolver import ChildResolverError, ResolverError


class DirectoryTree:
    """
    Class for creating and managing a directory tree
    """

    def __init__(self):
        self.directory_tree = Node('Root')
        self.resolver = Resolver("name")
        self.path_mapping = {}

    def print_tree(self) -> None:
        """
        Print the structure of the current directory tree
        :return: None
        """
        print(RenderTree(self.directory_tree).by_attr())

    def build(self, file_list: [str], result_structure: str) -> None:
        """
        Creates a directory tree using the given file list
        :param file_list: the list of files that will be put in the tree
        :param result_structure: a string describing the output format from the tree. either "flat" or "mirror"
        :return: None
        """
        for folder_name, files in file_list:
            Node(folder_name, self.directory_tree)
            sub_tree = self._build_tree(files, result_structure)
            backend_root_node: Node = self.resolver.get(self.directory_tree, f'/Root/{folder_name}')
            for child in sub_tree.children:
                child.parent = backend_root_node

    def is_file(self, path: str) -> bool:
        """
        Determines whether the given path inside the directory tree is a file or not
        :param path: path to the element
        :return: True if the given path is a file, False otherwise
        """
        logging.info(f"is file path {path}")
        path_node: Node = self.resolver.get(self.directory_tree, path)
        return len(path_node.children) == 0

    def get_original_path(self, path: str) -> str:
        """
        Returns the original file path for a path. This can be used to retrieve the original location of a
        file that is displayed in a flat hierarchy
        :param path: path to the file
        :return: The original file path
        """
        return self.path_mapping.get(path, path)

    def get_children(self, path: str) -> List[str]:
        """
        Collects the children (files) of a given path (to a directory)
        :param path: path to the directory
        :return: a list of all the children
        """
        path = path[1:]  # strip leading "/"
        path_node: Node = self.resolver.get(self.directory_tree, path)
        children = []
        for child in path_node.children:  # type: Node
            children.append(child.name)
        return children

    def resolve(self, path: str) -> Node:
        """
        Gets the anytree Node that corresponds to a certain file path
        :param path: path to the node
        :return: the Node for the given path
        """
        node: Node = self.resolver.get(self.directory_tree, path)
        return node

    def contains(self, path: str) -> bool:
        """
        Check whether or not a certain element (file/directory) exists in the tree
        :param path: path to the element
        :return: True if the element exists, false otherwise
        """
        try:
            self.resolver.get(self.directory_tree, path)
            return True
        except (ChildResolverError, ResolverError):
            return False

    def _build_tree(self, files: [str], result_structure: str) -> Node:
        """
        Create a tree from a given list of files, and for a given structure type (mirror or flat)
        :param files: list of the files
        :param result_structure: either "mirror" or "flat"
        :return: the root Node of the created tree
        """
        if result_structure == 'mirror':
            return self._build_tree_mirror(files)
        elif result_structure == 'flat':
            return self._build_tree_flat(files)

    @staticmethod
    def _build_tree_mirror(file_paths: [str]) -> Node:
        """
        Creates a directory tree from the given files, where the structure of the tree mimics the
        original structure of the files
        :param file_paths: list of the files to be included in the tree
        :return: the root anytree.Node of the new tree
        """
        root_node = Node("Root")
        resolver = Resolver("name")
        file_paths = [path.split("/")[1:] for path in file_paths]
        max_index = _length_of_longest_path(file_paths)

        for i in range(max_index):
            # In every iteration of the outer loop we only work on parts up to position i
            for file_path in file_paths:
                if i >= len(file_path):
                    # After reaching the last part of a path it can be skipped
                    continue
                last_path_node = file_path[i]
                path_without_last_node = _create_path_from_parts(file_path[:i])
                parent_node = resolver.get(root_node, path_without_last_node)
                if not _parent_has_child(parent_node, last_path_node):
                    Node(last_path_node, parent_node)
        return root_node

    def _build_tree_flat(self, file_paths: [str]) -> Node:
        """
        Creates a directory tree from the given files, where all the files are put in a flat hierarchy
        :param file_paths: list of the files to be included in the tree
        :return: the root anytree.Node of the new tree
        """
        root_node = Node("Root")
        for path in file_paths:
            file = path.split('/')[-1]
            self.path_mapping[file] = path
            Node(file, parent=root_node)
        return root_node


def _create_path_from_parts(path_parts: List[str]) -> str:
    """Creates the typical path format from a list of the individual parts
    Example: ['home', 'usr', 'dir1'] => 'home/usr/dir'
    """
    return '/'.join(path_parts)


def _parent_has_child(parent_node: Node, name: str) -> bool:
    """Tests if the parent node has a child with the name given by the second argument"""
    for child in parent_node.children:
        if child.name == name:
            return True
    return False


def _length_of_longest_path(file_paths: List[List[str]]) -> int:
    """Determines the length of the longest path out of all the paths"""
    lengths_of_paths = [len(path) for path in file_paths]
    return max(lengths_of_paths, default=0)
