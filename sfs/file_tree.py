# Python imports

# 3rd party imports
from anytree import Node, Resolver, RenderTree
from typing import List
import logging
# Local imports


class DirectoryTree:

    def __init__(self, algorithm='default'):
        self.algorithm = algorithm
        self.directory_tree = Node('Root')
        self.resolver = Resolver("name")

    def printTree(self):
        print(RenderTree(self.directory_tree))

    def build_out(self, file_list):
        for backend_name, files in file_list:
            Node(backend_name, self.directory_tree)
            if backend_name == 'passthrough':
                tree = files
            elif backend_name == 'mdh':
                tree = build_tree(files)
            else:
                return
            backend_root_node: Node = self.resolver.get(self.directory_tree, f'/Root/{backend_name}')
            for child in tree.children:
                child.parent = backend_root_node

    def is_file(self, path):
        path = path[1:]  # strip leading "/"
        path_node: Node = self.resolver.get(self.directory_tree, path)
        return len(path_node.children) == 0

    def get_children(self, path):
        path = path[1:]  # strip leading "/"
        path_node: Node = self.resolver.get(self.directory_tree, path)

        children = [".", ".."]
        child: Node
        for child in path_node.children:
            children.append(child.name)
        return children


def build_tree(file_paths):
    root_node = Node("Root")
    parent_finder = Resolver("name")
    max_index = _length_of_longest_path(file_paths)
    for i in range(max_index):
        # In every iteration of the outer loop we only work on parts up to position i
        for file_path in file_paths:
            if i >= len(file_path):
                # After reaching the last part of a path it can be skipped
                continue
            last_path_node = file_path[i]
            path_without_last_node = _create_path_from_parts(file_path[:i])
            parent_node = parent_finder.get(root_node, path_without_last_node)
            if not _parent_has_child(parent_node, last_path_node):
                Node(last_path_node, parent_node)
    return root_node


def _create_path_from_parts(path_parts: List[str]) -> str:
    """Creates the typical path format from a list of the individual parts
    Example:
        > path_parts = ['home', 'usr', 'dir1']
        > _create_path_from_parts(path_parts)
        'home/usr/dir'
    """
    return '/'.join(path_parts)


def _parent_has_child(parent_node: Node, name: str) -> bool:
    """Tests if the parent node has a child with the name given by the second argument"""
    for child in parent_node.children:
        if child.name == name:
            return True
    return False


def _length_of_longest_path(file_paths: List[List[str]]) -> int:
    """Determines the length of the longest path out of all the paths
    Example:
        > file_paths = [['home', 'usr', 'dir1'], ['home', 'usr', 'dir2', 'file1'], ['home' , 'usr2']]
        > _length_of_longest_path(file_paths)
        4
    """
    lengths_of_paths = [len(path) for path in file_paths]
    return max(lengths_of_paths, default=0)
