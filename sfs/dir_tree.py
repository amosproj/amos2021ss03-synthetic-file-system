# Python imports

# 3rd party imports
import anytree.resolver
from anytree import Node, Resolver, RenderTree
from typing import List


class DirectoryTree:

    def __init__(self, algorithm='default'):
        self.algorithm = algorithm
        self.directory_tree = Node('Root')
        self.resolver = Resolver("name")

    def print_tree(self) -> None:
        print(RenderTree(self.directory_tree).by_attr())

    def build(self, file_list) -> None:
        for backend_name, files in file_list:

            Node(backend_name, self.directory_tree)
            sub_tree = build_tree(files)
            backend_root_node: Node = self.resolver.get(self.directory_tree, f'/Root/{backend_name}')
            for child in sub_tree.children:
                child.parent = backend_root_node

    def is_file(self, path) -> bool:
        #  path = path[1:]  # strip leading "/"
        logging.error(f"is file path {path}")
        path_node: Node = self.resolver.get(self.directory_tree, path)
        return len(path_node.children) == 0

    def get_children(self, path) -> List[str]:
        path = path[1:]  # strip leading "/"
        path_node: Node = self.resolver.get(self.directory_tree, path)
        children = [".", ".."]
        for child in path_node.children:  # type: Node
            children.append(child.name)
            print(f"added node: {child.name}")
        return children

    def contains(self, path) -> bool:
        try:
            path_node: Node = self.resolver.get(self.directory_tree, path)
            return True
        except (anytree.resolver.ChildResolverError, anytree.resolver.ResolverError):
            return False


def build_tree(file_paths) -> Node:
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
