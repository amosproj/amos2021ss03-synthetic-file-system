# Python imports
import logging
from string import Template
from typing import Callable, Dict, List

# 3rd party imports
from mdh import query
from mdh.errors import StateError, APIError, GraphQLSyntaxError

"""
File that contains some utility functions needed by the MDH backend
"""


class MDHQuery:

    def __init__(self, core: str):
        """
        Constructor, sets up the information for the query
        :param core: name of the mdh core
        """
        self.core = core
        self.result = None

    def send_request_and_get_result(self, query_file_path: str) -> Dict:
        """
        sends the query for retrieving the files to the MDH
        :return: dict
        """
        assert query_file_path is not None

        try:
            self.result = query.query(self.core, query_file_path)
        except (StateError, APIError, ConnectionError):
            raise
        except FileNotFoundError:
            if self.result:
                logging.exception("FileNotFoundError -> fallback to previous result")
            else:
                raise
        except GraphQLSyntaxError:
            if self.result:
                logging.exception("GraphQLSyntaxError -> fallback to previous result")
            else:
                raise

        return self.result


class QueryTemplates:
    """
    Class that contains functions that build the graphql query that has to be sent to the MDH
    """
    QUERY_TEMPLATE = Template(
        '''
        query {
            searchMetadata (
                    filterFunctions: $filterFunctions
                    filterLogicOption: $filterLogicOption,
                    selectedTags: $selectedTags,
                )   {
                totalFilesCount,
                returnedFilesCount,
                instanceName,
                timeZone,
                fixedReturnColumnSize,
                dataTypes {
                    name,
                    type,
                }
                files {
                    id,
                    metadata {
                        name,
                        value,
                    }
                }
            }
        }
        ''')
    DEFAULT_VALUES = {
        'selectedTags': ["FileName", "FileSize", "MIMEType", "FileInodeChangeDate", "SourceFile"],
        'filterLogicOption': 'AND'
    }

    @classmethod
    def create_query(cls, variables: Dict):
        """
        Creates a query from the template using the given variables
        :param variables: the variables that will be plugged into the template
        :return: the graphql query
        """
        template = cls.QUERY_TEMPLATE
        variables = cls._convert_to_graphql_vars(variables)
        return template.safe_substitute(variables).replace("'", '"')

    @classmethod
    def _convert_to_graphql_vars(cls, query_options: Dict) -> Dict:
        """
        Takes some query options and translates them into graphql variables
        :param query_options:
        :return:
        """
        graphql_vars = cls.DEFAULT_VALUES.copy()
        for key, value in query_options.items():
            if key not in ['filterFunctions', 'filterLogicOption']:
                continue
            parse = _get_parse_function(key)
            value = parse(value)
            graphql_vars.update({key: value})
        return graphql_vars


def _parse_filter_functions(raw_filter_functions: List[Dict]) -> str:
    """
    Takes a list of filter functions and puts them into the proper graphql format needed for the query
    :param raw_filter_functions: list of the filter functions
    :return: the translated function
    """
    filter_functions = '['
    for raw_filter_function in raw_filter_functions:
        tag, operation, value = raw_filter_function
        filter_function = f'{{tag: "{tag}", operation: {operation}, value: "{value}"}},'
        filter_functions += filter_function

    filter_functions += ']'
    print(filter_functions)
    return filter_functions


def _parse_filter_logic_option(option: str) -> str:
    """
    Parses the filter logic options into a string (?) TODO
    :param option:
    :return:
    """
    if option in ['AND', 'OR']:
        return option
    if option == 'INDIVIDUAL':
        raise NotImplementedError()


def _get_parse_function(key: str) -> Callable:
    """
    Retrieves the parse function for the given key
    :param key: name of the function
    :return: the parse function
    """
    parse_functions = {
        'filterFunctions': _parse_filter_functions,
        'filterLogicOption': _parse_filter_logic_option
    }
    return parse_functions[key]
