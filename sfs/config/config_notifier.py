# 3rd party imports
from pyinotify import Event, ProcessEvent

# Local import
from sfs.backend.mdh import MDHQueryRoot
from sfs.paths import CONFIG_FILE_PATH


class ConfigFileEventHandler(ProcessEvent):
    """
    Event handler that gets triggered when the "config.graphql" file changes. If this happens, this class is
    responsible for updating the directory tree, according to the new filters
    """

    def __init__(self, fuse, core_name: str, **kargs):
        """
        Constructor for the class. For more information see pyinotify.ProcessEvent.__init()__
        :param fuse: mdh_fuse for which the directory tree will be updated
        :param core_name: for corresponding core
        :param kargs: optional arguments for the pyinotify.ProcessEvent constructor
        """
        super().__init__(**kargs)
        self.core_name = core_name
        self.fuse = fuse

    def update_tree(self) -> None:
        """
        Update the directory tree in the fuse, according to the new config
        :return: Nothing
        """

        print("Updating the directory tree")
        query_root = MDHQueryRoot(self.core_name, CONFIG_FILE_PATH)
        query_root.send_request_get_result()

        self.fuse.metadatahub_files = query_root.result['searchMetadata']['files']
        self.fuse.directory_tree = build_tree_from_files(self.fuse.metadatahub_files)

    def process_IN_MODIFY(self, event: Event) -> None:
        """
        Called when a IN_MODIFY event is triggered on the config file
        :param event: see parent class documentation; unused
        :return: Nothing
        """
        # TODO: Correct handling for modified files
        #self.update_tree()
