# Python imports
from string import Template
from typing import Callable, Dict, List

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


class QueryTemplates:
    QUERY_TEMPLATE = Template(
        '''
        query {
            searchMetadata (
                    filterFunctions: $filterFunctions
                    filterLogicOption: $filterLogicOption,
                    $filterLogicIndividual
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
    def create_query(cls, vars):
        template = cls.QUERY_TEMPLATE
        variables = cls._convert_to_graphql_vars(vars)
        return template.safe_substitute(variables).replace("'", '"')

    @classmethod
    def _convert_to_graphql_vars(cls, query_options: Dict) -> Dict:
        graphql_vars = cls.DEFAULT_VALUES.copy()
        graphql_vars["filterLogicIndividual"] = ""

        for key, value in query_options.items():
            if key not in ['filterFunctions', 'filterLogicOption', 'filterLogicIndividual']:
                continue
            parse = _get_parse_function(key)
            value = parse(value)
            graphql_vars[key] = value

        return graphql_vars


def _parse_filter_functions(raw_filter_functions: List[Dict]) -> str:
    filter_functions = '['
    for raw_filter_function in raw_filter_functions:
        tag, operation, value = raw_filter_function
        filter_function = f'{{tag: "{tag}", operation: {operation}, value: "{value}"}},'
        filter_functions += filter_function

    filter_functions += ']'

    return filter_functions


def _parse_filter_logic_option(option: str) -> str:
    return option


def _parse_filter_logic_individual(option: str) -> str:
    return f'filterLogicIndividual: "{option}",'


def _get_parse_function(key: str) -> Callable:
    parse_functions = {
        'filterFunctions': _parse_filter_functions,
        'filterLogicOption': _parse_filter_logic_option,
        'filterLogicIndividual': _parse_filter_logic_individual
    }
    return parse_functions[key]
