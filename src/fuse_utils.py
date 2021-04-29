from logging import root

from anytree import *
from send_mdh_request import *

"""
md_res = MetadataResult()
md_res.files = File()
md_res.files.dir_path = True
md_res.files.name = True
md_query = MetadataQuery(md_res)

result = md_query.build_and_send_request()  # type: MetadataResult
metadatahub_files = result.files
"""


# Takes a list of files and turns them into a directory tree starting at a "root" node
def build_tree_from_files(files: [File]):
    root_node = Node("Root")

    # prepare directory names for easier processing
    file_paths = []
    for file in files:
        full_file_name = file.dir_path + "/" + file.name
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
            parent_node: Node = None
            parent_node = parent_finder.get(root_node, prev_path)
            for child in parent_node.children:
                if child.name == path_part:
                    has_child = True
            if not has_child:
                new_node = Node(path_part, parent_node)
        if num_files_to_parse <= 0:
            break
        i += 1

    return root_node
