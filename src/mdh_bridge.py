# Python imports
import copy
import os
from enum import Enum

# 3rd party imports
import mdh
import requests

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


class MDHQueryRoot:

    def __init__(self, core: str, query_file: str):
        self.core = core
        self.query_file = query_file
        self.result = None

    def build_and_send_request(self) -> None:
        self.result = mdh.query.query(self.core, self.query_file)


if __name__ == "__main__":

    graphql_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "search_mdh.graphql")

    mdh.init()
    mdhqueryroot = MDHQueryRoot("core-sfs", graphql_path)
    mdhqueryroot.build_and_send_request()
    print(mdhqueryroot.result['searchMetadata']['totalFilesCount'])
