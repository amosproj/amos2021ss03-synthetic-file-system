from anytree import *
from mdh_bridge import *



def build_tree_from_files(files: [MDHFile]):
    """
    build_tree_from_files Turns a list of FilePaths into a directory tree. The tree is built upon a "Root" node
    :param files: a list of file paths e.g ["/metadatahub/crawler/test", "/metadatahub/docs/test", ...]
    :return: The root Node (anytree.Node) of the resulting tree
    """

    root_node = Node("Root")

    # prepare directory names for easier processing
    file_paths = []
    for file in files:
        dir_path = ""
        file_name = ""
        for metadata in file.metadata:  # type: MDHMetadatum
            if metadata.name == "Directory":
                dir_path = metadata.value
            if metadata.name == "FileName":
                file_name = metadata.value

        full_file_name = dir_path + file_name
        file_paths.append(full_file_name.split("/"))

    i = 1
    num_files_to_parse = len(file_paths)
    while True:
        for file_path in file_paths:
            if i >= len(file_path):
                num_files_to_parse -= 1
                continue
            path_part = file_path[i]
            prev_path = ""
            for j in range(1, i):
                prev_path += file_path[j] + "/"

            prev_path = prev_path[:len(prev_path) - 1]  # remove trailing "/"

            has_child = False
            parent_finder = Resolver("name")
            parent_node: Node
            parent_node = parent_finder.get(root_node, prev_path)
            for child in parent_node.children:
                if child.name == path_part:
                    has_child = True
            if not has_child:
                Node(path_part, parent_node)
        if num_files_to_parse <= 0:
            break
        i += 1

    return root_node
