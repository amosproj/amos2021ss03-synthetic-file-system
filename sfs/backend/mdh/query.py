# 3rd party imports
from mdh import query
from mdh.errors import StateError, APIError, GraphQLSyntaxError


class MDHQueryRoot:

    def __init__(self, core: str, query_file: str):
        self.core = core
        self.query_file = query_file
        self.result = None

    def send_request_get_result(self) -> None:
        try:
            self.result = query.query(self.core, self.query_file)
        # TODO: Error handling
        except StateError:
            raise
        except APIError:
            raise
        except ConnectionError:
            raise
        except FileNotFoundError:
            raise
        except GraphQLSyntaxError:
            raise
