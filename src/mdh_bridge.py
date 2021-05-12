
import copy
import requests
import json
from enum import Enum

"""
harvest queries ang query builder queries are not implemented! No idea if/when they will come
Objects in query arguments are not supported so fat :(
"""

"""
This class allows for easy communication with the Metadatahub webql. For this it offers classes, mirroring
every query or object that can be used in the MDH. All of these classes inherit MDHObject, which offers
functionality to (de-)serialize the contents from the class into a query, or the result of a query into the classes.
All Queries inherit from MDHQuery, which implements a different serialization algorithm.
The usage of this functionality can be broken down into a few steps:
1. Set up a MDHQueryRoot class. This class contains a list of queries that will be executed in the MDH.
    query_root = MDHQueryRoot()
2. Set up an MDHQuery. For this you have to create some new Query, like this:
    query = MDHQuery_searchMetadata()
Every query has some flags as their members, which are default set to False. When they are set to another value, that
value is used as an argument for their query. For example, when you only want to search metadata with a certain fileId:
    query.fileIds = [1, 2, 3, 4, 5]
3. Set the result field of the Query: For every query, the result field has to be specified. This field is repsonsible,
for telling the MDH which of the resulting objects attributes you actually want to get returned. For example, if you
only want to see the total number of results and all the metadata for all the resulting classes, use the following:
    query.result.totalFilesCount = True
    query.result.files = MDHFile()
    query.result.files.metadata = MDHMetadata()
    query.result.files.metadata.metadatum.name = True
    query.result.files.metadata.metadatum.value = True
4. Add the query to the query_root and execute it:
    query_root.queries.append(query)
    query_root.build_and_send_request()
5. Access the queries results:
    total_file_count = query_root.queries[0].result.totalFilesCount
    ...
"""

MetadataOption = Enum("MetadataOption",
                      "NOT_CONTAINS EQUAL NOT_EQUAL GREATER SMALLER EXISTS NOT_EXISTS EMPTY NOT_EMPTY")
LogicOption = Enum("LogicOption", "AND OR INDIVIDUAL")
SortByOption = Enum("SortByOption", "ASC DESC")

session = requests.session()
session.headers["X-Authorization-Bearer"] = "admin"


class MDHObject:

    def serialize(self):
        # Get all members of the object
        attributes = [attr for attr in dir(self) if not callable(
            getattr(self, attr)) and not attr.startswith("_") and attr not in ["query_name", "result"]]

        query = ""
        # Enumerate over all arguments and add them to the query
        for i, attribute in enumerate(attributes):
            value = getattr(self, attribute)

            if value:
                if isinstance(value, MDHObject):
                    attribute = attribute + "{" + value.serialize() + "}"

                query += f"{attribute}" + "\n"

        return query

    def deserialize(self, json: dict):

        for entry in json.keys():
            if not isinstance(json[entry], list):
                attribute = getattr(self, entry)
                if isinstance(attribute, MDHObject):
                    attribute.deserialize(json[entry])
                else:
                    setattr(self, entry, json[entry])

            else:
                attribute = getattr(self, entry)
                if isinstance(attribute, MDHObject):
                    new_attribute = []
                    for e in json[entry]:
                        new_attribute_entry = copy.deepcopy(attribute)
                        new_attribute_entry.deserialize(e)
                        new_attribute.append(new_attribute_entry)
                    setattr(self, entry, new_attribute)
                else:
                    setattr(self, entry, json[entry])


class MDHQuery(MDHObject):
    query_name = ""
    result: MDHObject = None

    def serialize(self):
        query = self.query_name

        # Get all members of the Query
        attributes = [attr for attr in dir(self) if not callable(
            getattr(self, attr)) and not attr.startswith("_") and attr not in ["query_name", "result"]]

        has_arguments = False

        argument_string = ""
        # Enumerate over all arguments and add them to the query
        for i, attribute in enumerate(attributes):
            value = getattr(self, attribute)

            if value:
                if isinstance(value, MDHObject):
                    value = "{" + value.serialize() + "}"

                argument_string += f" {attribute}: {value} "
                has_arguments = True
                if not i == len(attributes) - 1:
                    query += ", "

        # if arguments are given add them to the query
        if has_arguments:
            query += "(" + argument_string + ")"

        # At this point the query function has been built
        # Next we have to add the results filter
        query += "{" + self.result.serialize() + "}"
        return query

    def deserialize(self, json):
        return self.result.deserialize(json)


class MDHMetadatatagDataType(MDHObject):
    name: bool or str = False
    type: bool or str = False


class MDHFileType(MDHObject):
    name: bool or str = False
    fileCount: bool or int = False
    mimeType: bool or str = False
    metadataCount: bool or int = False
    metadataCountAggregatedValues: bool or int


class MDHMimeType(MDHObject):
    name: bool or str = False
    fileCount: bool or int = False
    fileTypes: bool or [MDHFileType] = False


class MDHMetadatum(MDHObject):
    name: bool or str = False
    value: bool or str = False


class MDHMetadata(MDHObject):
    name: bool or str = False
    count: bool or int = False
    type: bool or str = False
    searchDeactivated: bool = False  # TODO
    virtual: bool = False  # TODO
    # randomExample  NOT IMPLEMENTED YET


class MDHFileTypeStat(MDHObject):
    name: bool or str = False
    count: bool or int = False


class MDHSystemInfo(MDHObject):
    instanceName: bool or str = False
    currentUserRole: bool or str = False
    hostSystem: bool or str = False
    installTime: bool or str = False  # TODO maybe use proper time types?
    lastReboot: bool or str = False
    scannedFiles: bool or int = False
    harvestedFiles: bool or int = False
    differentFileTypes: bool or int = False
    harvestedMetadata: bool or int = False
    differentMetadata: bool or int = False
    treewalkState: bool or str = False
    lastExecutedTreewalk: bool or str = False
    nextScheduledTreewalk: bool or str = False
    versionExtractorTreewalk: bool or str = False
    versionMetadataHub: bool or str = False
    versionBuild: bool or str = False
    isDeveloperMode: bool = False  # TODO
    instanceDescription: bool or str = False
    topFileTypes: bool or [MDHFileTypeStat] = False


class MDHServerState(MDHObject):
    state: bool or int = False
    runningSince: bool or int = False


class MDHFilterFunction(MDHObject):
    tag: bool or str = False
    value: bool or str = False
    operation: bool or MetadataOption = False


class MDHSortFunction(MDHObject):
    sortBy: bool or str = False
    sortByOption: bool or SortByOption = False


class MDHQuery_systemInfo(MDHQuery):
    query_name = "systemInfo"
    result = MDHSystemInfo()


class MDHQuery_getServerState(MDHQuery):
    query_name = "getServerState"
    result = MDHServerState()


class MDHQuery_getMetadataTags(MDHQuery):
    fileTypeScope: bool or str = False
    mimeTypeScope: bool or str = False
    nameFilter: bool or str = False
    excludeMetadata: bool or str = False
    limit: bool or int = False
    offset: bool or int = False

    query_name = "getMetadataTags"
    result: [MDHMetadata] = []


class MDHQuery_getFileTypes(MDHQuery):
    excludeFileType: bool or str = False
    excludeMimeType: bool or str = False
    nameFilter: bool or str = False
    limit: bool or int = False
    offset: bool or int = False

    query_name = "getFileTypes"
    result: [MDHFileType] = []


class MDHQuery_getMimeTypes(MDHQuery):
    excludeMimeType: bool or str = False
    nameFilter: bool or str = False
    limit: bool or int = False
    offset: bool or int = False

    query_name = "getMimeTypes"
    result: [MDHMimeType] = []


class MDHQuery_getMetadata(MDHQuery):
    fileTypeScope: bool or str = False
    mimeTypeScope: bool or str = False
    name: bool or str = False

    query_name = "getMetadata"
    result = MDHMetadata()


class MDHQuery_getFileType(MDHQuery):
    name: bool or str = False

    query_name = "getFileType"
    result = MDHFileType()


class MDHQuery_getMimeType:
    name: bool or str = False

    query_name = "getMimeType"
    result = MDHMimeType()


class MDHFile(MDHObject):
    id: bool or str = False
    metadata: bool or MDHMetadata or [MDHMetadatum] = False


class MDHResultSet(MDHObject):
    fromIndex: bool or int = False
    toIndex: bool or int = False
    totalFilesCount: bool or int = False
    returnedFilesCount: bool or int = False
    timeZone: bool or str = False
    instanceName: bool or str = False
    fixedReturnColumnSize: bool = False  # TODO how do we do this here?
    graphQLQuery: bool or str = False
    graphQLVariables: bool or str = False
    files: bool or MDHFile or [MDHFile] = False
    graphQLDebug: bool or str = False
    dataTypes: bool or MDHMetadatatagDataType or [MDHMetadatatagDataType] = False


class MDHQuery_searchMetadata(MDHQuery):
    fileIds: bool or [int] = False
    filterFunctions: bool or [MDHFilterFunction] = False
    filterLogicOption: bool or LogicOption = False
    sortFunctions: bool or [MDHSortFunction] = False
    filterLogicalIndividual: bool or str = False
    limit: bool or int = False
    offset: bool or int = False
    fileSizeAsHumanReadable: bool = False  # TODO how do we do this with bool values?
    convertDateTimeTo: bool or str = False
    _selectedTags: bool or [str] = False

    @property
    def selectedTags(self) -> bool or [str]:
        if self._selectedTags and isinstance(self._selectedTags, bool):
            _selectedTags = []
            for dataType in self.result.dataTypes:
                _selectedTags.append(dataType.name)

            self._selectedTags = _selectedTags

        return self._selectedTags

    @selectedTags.setter
    def selectedTags(self, selectedTags) -> None:
        self._selectedTags = selectedTags

    result = MDHResultSet()
    query_name = "searchMetadata"


class MDHQueryRoot:

    def __init__(self):
        self.queries: [MDHQuery] = []

    def serialize(self):
        query = "query {"

        for sub_query in self.queries:  # type: MDHQuery
            query += sub_query.serialize()

        query += "}"
        return query

    def deserialize(self, json_string: str):

        data_json: dict = json.loads(json_string)["data"]  # TODO ERRORS
        for query in self.queries:  # type: MDHQuery
            query_json = data_json[query.query_name]
            query.deserialize(query_json)

    def build_and_send_request(self, url="http://localhost:11000/graphql"):
        """
        Serializes this classes content into a webql request and sends it to the metadatahub web service
        :param url: The url the metadatahub is running
        :return: The deserialized json result of the query
        """
        query = self.serialize()
        result = session.post(url, json={"query": query})
        self.deserialize(result.text)


"""
temporary test case for the bridge and the fuse_utils; IGNORE
TODO: remove this when a proper test case has been written
if __name__ == '__main__':
    query_root = MDHQueryRoot()
    query = MDHQuery_searchMetadata()
    query.result.files = MDHFile()
    query.result.files.metadata = MDHMetadatum()
    query.result.files.metadata.value = True
    query.result.files.metadata.name = True
    query_root.queries.append(query)
    query_root.build_and_send_request()
    metadatahub_files = query_root.queries[0].result.files
    import fuse_utils
    from anytree import RenderTree
    directory_tree = fuse_utils.build_tree_from_files(metadatahub_files)
    print(RenderTree(directory_tree))
    rq = MDHQueryRoot()
    q = MDHQuery_searchMetadata()
    q.result.toIndex = True
    f = MDHFile()
    f.id = True
    f.metadata = MDHMetadatum()
    f.metadata.name = True
    f.metadata.value = True
    q.result.files = f
    q.fileIds = [13, 69, 420]
    rq.queries.append(q)
    query2 = MDHQuery_getServerState()
    query2.result.runningSince = True
    rq.queries.append(query2)
    query3 = MDHQuery_systemInfo()
    query3.result.harvestedFiles = True
    rq.queries.append(query3)
    rq.build_and_send_request()
    print(rq.serialize())
"""
