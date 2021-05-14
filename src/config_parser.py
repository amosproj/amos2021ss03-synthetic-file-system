import os.path

from mdh_bridge import *
import toml
import pyinotify




def setup(config_path: str, event_handler: pyinotify.ProcessEvent):
    watch_manager = pyinotify.WatchManager()
    watch_manager.add_watch(os.path.abspath(config_path), pyinotify.ALL_EVENTS, rec=True)

    # notifier
    notifier = pyinotify.Notifier(watch_manager, event_handler)
    notifier.loop()


def create_query_from_config(config_path: str) -> MDHQuery_searchMetadata:
    with open(config_path, "r") as config_file:
        content = config_file.read()
        print(content)
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
        search_Query.filterLogicOption = LogicOption.AND
        return search_Query



"""
search_Query = MDHQuery_searchMetadata()
    filterfunc = MDHFilterFunction()
    filterfunc.value = "DME-30521-7.jpeg"
    filterfunc.tag = "FileName"
    filterfunc.operation = MetadataOption.EQUAL

    filterfunc2 = MDHFilterFunction()
    filterfunc2.value = "JPEG"
    filterfunc2.tag = "FileType"
    filterfunc2.operation = MetadataOption.EQUAL
    search_Query.filterLogicOption = LogicOption.AND
    print(filterfunc2.serialize())

    search_Query.filterFunctions = [filterfunc, filterfunc2]
    print(search_Query.serialize())
    """