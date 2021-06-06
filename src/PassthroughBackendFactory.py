from BackendFactory import BackendFactory
from MDHBackend import MDHBackend
from BackendFactoryManager import BackendFactoryManager
from anytree import RenderTree, Node, Resolver
import fuse_utils
from PassthroughBackend import PassthroughBackend

import glob

# root_dir needs a trailing slash (i.e. /root/dir/)


class PassthroughBackendFactory(BackendFactory):
    """
    Implementation of the PassthroughBackend.
    This Factory will create PassthroughBackend for given sections.
    See PassthroughBackend for more information
    """

    def __init__(self):
        super().__init__()

    def create_backend_from_section(self, instance_cfg) -> MDHBackend:
        target_dir = instance_cfg['path']

        def create_file_tree(target_dir):
            file_paths = []
            for filename in glob.iglob(target_dir + "**",
                                       recursive=True):
                file_paths.append(filename.split("/")[1:])

            root_node = Node("Root")
            parent_finder = Resolver("name")

            max_index = fuse_utils._length_of_longest_path(file_paths)
            for i in range(max_index):
                # In every iteration of the outer loop we only work on parts up to position i
                for file_path in file_paths:
                    if i >= len(file_path):
                        # After reaching the last part of a path it can be skipped
                        continue
                    last_path_node = file_path[i]
                    path_without_last_node = fuse_utils._create_path_from_parts(file_path[:i])
                    parent_node = parent_finder.get(root_node, path_without_last_node)
                    if not fuse_utils._parent_has_child(parent_node, last_path_node):
                        Node(last_path_node, parent_node)
            return root_node

        directory_tree = create_file_tree(target_dir)

        #print(RenderTree(directory_tree))
        #print("created dir tree!")

        backend = PassthroughBackend(directory_tree)

        return backend


#PassthroughBackendFactory().create_backend_from_section("")


# auto register backend
BackendFactoryManager().register_backend_factory(PassthroughBackendFactory(), "PT")
