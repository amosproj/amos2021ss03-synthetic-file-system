# Python imports
import logging
from typing import List

# 3rd party imports
from anytree import Node, Resolver, RenderTree
from anytree.resolver import ChildResolverError, ResolverError


class DirectoryTree:

    def __init__(self):
        self.directory_tree = Node('Root')
        self.resolver = Resolver("name")
        self.path_mapping = {}

    def print_tree(self) -> None:
        print(RenderTree(self.directory_tree).by_attr())

    def build(self, file_list, result_structure: str) -> None:
        for backend_name, files in file_list:
            Node(backend_name, self.directory_tree)
            sub_tree = self.build_tree(files, result_structure)
            backend_root_node: Node = self.resolver.get(self.directory_tree, f'/Root/{backend_name}')
            for child in sub_tree.children:
                child.parent = backend_root_node

    def is_file(self, path) -> bool:
        #  path = path[1:]  # strip leading "/"
        logging.error(f"is file path {path}")
        path_node: Node = self.resolver.get(self.directory_tree, path)
        return len(path_node.children) == 0

    def get_original_path(self, path):
        return self.path_mapping.get(path, path)

    def get_children(self, path) -> List[str]:
        path = path[1:]  # strip leading "/"
        path_node: Node = self.resolver.get(self.directory_tree, path)
        children = []
        for child in path_node.children:  # type: Node
            children.append(child.name)
            print(f"added node: {child.name}")
        return children

    def resolve(self, path) -> Node:
        node = self.resolver.get(self.directory_tree, path)
        return node

    def contains(self, path) -> bool:
        try:
            self.resolver.get(self.directory_tree, path)
            return True
        except (ChildResolverError, ResolverError):
            return False

    def build_tree(self, files, resultStructure: str) -> Node:
        if resultStructure == 'mirror':
            return self.build_tree_mirror(files)
        elif resultStructure == 'flat':
            return self.build_tree_flat(files)

    def build_tree_mirror(self, file_paths) -> Node:
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

    def build_tree_flat(self, file_list):
        root_node = Node("Root")
        print(file_list)
        for path in file_list:
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
