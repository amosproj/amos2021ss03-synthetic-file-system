from BackendFactory import BackendFactory
from Backend import Backend
from MDHBackend import MDHBackend
from BackendFactoryManager import BackendFactoryManager
from mdh_bridge import *
from anytree import Node, RenderTree
import fuse_utils
import paths

_QUERY = " \
\
query {\
  searchMetadata {\
    files {\
      metadata {\
        value\
        name\
      }\
    }\
  }\
}"


class MDHBackendFactory(BackendFactory):

    def __init__(self):
        super().__init__()
        self.core_name = "core-test"

    def create_backend_from_section(self, section) -> MDHBackend:

        query_root = MDHQueryRoot(self.core_name, paths.CONFIG_FILE_PATH)
        query_root.send_request_get_result()

        mdh_files = query_root.result['searchMetadata']['files']
        directory_tree = fuse_utils.build_tree_from_files(mdh_files)

        print(RenderTree(directory_tree))
        print("created dir tree!")

        mdh_backend = MDHBackend(directory_tree)
        return mdh_backend


# auto register backend
BackendFactoryManager().register_backend_factory(MDHBackendFactory(), "MDH")
