# Python imports
import os

# 3rd party imports
import mdh


class MDHQueryRoot:

    def __init__(self, core: str, query_file: str):
        self.core = core
        self.query_file = query_file
        self.result = None

    def send_request(self) -> None:
        self.result = mdh.query.query(self.core, self.query_file)


if __name__ == "__main__":

    graphql_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "search_mdh.graphql")

    mdh.init()
    mdhqueryroot = MDHQueryRoot("core-sfs", graphql_path)
    mdhqueryroot.send_request()
    print(mdhqueryroot.result['searchMetadata']['totalFilesCount'])
