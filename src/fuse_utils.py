# 3rd party imports
from anytree import Node, Resolver
from typing import Dict, List


def build_tree_from_files(files: List[Dict]) -> Node:
    """Builds a directory tree out of the results from the metadata-hub query.
    The tree is build upon a "Root" node which is returned at the end.
    Each dict contains the entire result but only the file paths are used.

    Args:
        files (List[Dict]): list containing the results from the mdh query

    Returns:
        Node: The root node (anytree.Node) of the resulting tree
    """
    # '/home/dome_/test_tree'
    root_node = Node("Root")
    parent_finder = Resolver("name")
    file_paths = _extract_file_paths_parts(files)
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


def _extract_file_paths_parts(files: List[Dict]) -> List[List[str]]:
    """Extracts the file paths from each dict which contains the entire result

    Args:
        files (List[Dict]): list containing all results from the mdh.

    Returns:
        List[List[str]]: list containing only the paths. Each path is a list of its parts.
    """
    file_paths = []
    for file in files:
        full_file_path = ""
        for metadata in file['metadata']:
            if metadata['name'] == "SourceFile":
                full_file_path = metadata['value']
        file_paths.append(full_file_path)

    file_paths_parts = []
    for file_path in file_paths:
        # if file_path.startswith('/home/dome_/test_tree'):
        #    file_path = file_path[len('/home/dome_/test_tree'):]
        file_paths_parts.append(file_path.split("/")[1:])
    return file_paths_parts


def _create_path_from_parts(path_parts: List[str]) -> str:
    """Creates the typical path format from a list of the individual parts

    Args:
        path_parts (List[str]): list containing the parts of a path
                                Ex.: ['home', 'usr', 'dir1']
    Returns:
        str: Concatenation of the parts to a path format
             Ex..: home/usr/dir
    """
    return '/'.join(path_parts)


def _parent_has_child(parent_node: Node, name: str) -> bool:
    """Tests if the parent node has a child with the name given by the second argument

    Args:
        parent_node (Node): the parent node for the path without the last element given by name
        name (str): name corresponds to the last item of the path

    Returns:
        bool: True if the parent node has a child with the specified name
    """
    for child in parent_node.children:
        if child.name == name:
            return True
    return False


def _length_of_longest_path(file_paths: List[List[str]]) -> int:
    """Determines the length of the longest path out of all the paths

    Args:
        file_paths (List[List[str]]): a list containing all file paths which are lists of the parts
                Ex.: [['home', 'usr', 'dir1'], ['home', 'usr', 'dir2', 'file1'], ['home' , 'usr2']]

    Returns:
        int: The length of the longest path in the list - Ex.: 4
    """
    lengths_of_paths = [len(path) for path in file_paths]
    return max(lengths_of_paths, default=0)
