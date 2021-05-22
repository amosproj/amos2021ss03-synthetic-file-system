# 3rd party imports
from pyinotify import Event, ProcessEvent
from mdh_bridge import MDHQueryRoot

# Local import
from fuse_utils import build_tree_from_files


class ConfigFileEventHandler(ProcessEvent):
    """
    Event handler that gets triggered when the "config.cfg" file changes. If this happens, this class is
    responsible for updating the directory tree, according to the new filters
    """

    def __init__(self, fuse, core_name: str, config_path: str, **kargs):
        """
        Constructor for the class. For more information see pyinotify.ProcessEvent.__init()__
        :param fuse: mdh_fuse for which the directory tree will be updated
        :param kargs: optional arguments for the pyinotify.ProcessEvent constructor
        """
        super().__init__(**kargs)
        self.config_path = config_path
        self.core_name = core_name
        self.fuse = fuse

    def update_tree(self) -> None:
        """
        Update the directory tree in the fuse, according to the new config
        :return: Nothing
        """

        print("Updating the directory tree")
        query_root = MDHQueryRoot(self.core_name, self.config_path)
        query_root.send_request_get_result()

        self.fuse.metadatahub_files = query_root.result['searchMetadata']['files']
        self.fuse.directory_tree = build_tree_from_files(self.metadatahub_files)

    def process_IN_MODIFY(self, event: Event) -> None:
        """
        gets called when a IN_MODIFY event is triggered on the config file
        :param event: see parent class documentation; unused
        :return: Nothing
        """
        self.update_tree()
