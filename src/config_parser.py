# Python imports
import os.path

# 3rd party imports
import pyinotify
import toml

# Local imports
from mdh_bridge import MDHQuery_searchMetadata, MDHFilterFunction, MetadataOption, LogicOption


def setup(config_path: str, event_handler: pyinotify.ProcessEvent):
    """
    Sets up a watch via pyinotify that watches the given filepath. When some event happens at the given path, the
    event handler gets called
    :param config_path: file to the file that will be watched
    :param event_handler: The class which will be notified when something happens to the watched path
    :return: Nothing
    """
    watch_manager = pyinotify.WatchManager()
    watch_manager.add_watch(os.path.abspath(config_path), pyinotify.ALL_EVENTS, rec=True)
    notifier = pyinotify.Notifier(watch_manager, event_handler)
    notifier.loop()


def create_query_from_config(config_path: str) -> MDHQuery_searchMetadata:
    """
    Creates a MDHQuery_searchMetadata. This query will then be fed with the metadata filters specified in the
    config file. The config file has to be a TOML file, with a section "FILTER" where a 2d list filters lies.
    :param config_path: path to the config file from which the filters will be read
    :return: The Query
    """
    with open(config_path, "r") as config_file:
        content = config_file.read()
        filters = toml.loads(content)
        filter_arguments = []
        for filter in filters["FILTER"]["filters"]:
            filter_argument = MDHFilterFunction()
            filter_argument.tag = filter[0]
            filter_argument.value = filter[1]
            filter_argument.operation = MetadataOption[filter[2]]
            filter_arguments.append(filter_argument)

        search_Query = MDHQuery_searchMetadata()
        search_Query.filterFunctions = filter_arguments

        # for now we always AND the filters. We should probably add an option for this in the config file
        search_Query.filterLogicOption = LogicOption.AND
        return search_Query
