# Python imports
import shutil
import time
import unittest
from contextlib import ExitStack
from pathlib import Path

# 3rd party imports
import json
import mdh
from mdh.errors import GraphQLSyntaxError
from mdh.types import MDHCore

# Local imports
from sfs.backend.mdh import MDHQuery
from sfs.paths import GRAPHQL_QUERY_PATH


class TestMDHQuery(unittest.TestCase):

    file_path = None
    core_json_path = None
    cores_dir_path = None
    empty_graphql_query_path = None
    mdh_key = None
    mdh_key_lock = None
    core_name = None

    @classmethod
    def setUpClass(cls):
        # Setup needed paths
        cls.file_path = Path(__file__).parent
        cls.core_json_path = cls.file_path / "core.json"
        cls.cores_dir_path = cls.file_path / "cores"

        # Copy graphql file and empty it
        cls.empty_graphql_query_path = Path(shutil.copy(GRAPHQL_QUERY_PATH, cls.file_path))
        cls.empty_graphql_query_path.open('w').close()

        cls.mdh_key = cls.file_path / ".mdh"
        cls.mdh_key_lock = cls.file_path / ".mdh.lock"

        # Setup json file for a mdh core
        cls.core_name = "core-test"
        cls.core_json = {
            "name": cls.core_name,
            "version": "latest",
            "passwords": {
                "user": "user",
                "admin": "admin"
            },
            "directories": {
                str(cls.file_path): "Test"
            },
            "port": 11111,
            "database": "mdh-core-test-db"
        }
        with open(cls.core_json_path, 'w') as f:
            json.dump(cls.core_json, f)

    @classmethod
    def tearDownClass(cls):
        # Cleanup
        cls.core_json_path.unlink()
        shutil.rmtree(cls.cores_dir_path)
        cls.empty_graphql_query_path.unlink()
        cls.mdh_key.unlink()
        cls.mdh_key_lock.unlink()

        mdh.cores.stop(cls.core_name)

    def setUp(self):
        # create a context to ensure that cleanup is performed in case of failure
        with ExitStack() as stack:
            stack.callback(self.tearDownClass)

            mdh.init(self.file_path)

            mdh.cores.run(self.core_json, force=True)

            core = MDHCore.from_config(self.core_json)

            # Wait for the core to be started
            timeout = [1, 1, 2, 3, 5]  # Fibonacci timeout
            while timeout:
                try:
                    mdh.check_access(url=core.url, token=core.token)
                    break
                except ConnectionError:
                    time.sleep(timeout.pop())

            if not timeout:
                raise RuntimeError("Failed starting the MdH Core")

            stack.pop_all()

    def test_mdh_query_with_available_core_returns_result(self) -> None:
        result = MDHQuery(self.core_name).send_request_and_get_result(GRAPHQL_QUERY_PATH)

        self.assertEqual(result['searchMetadata']['totalFilesCount'], 0)
        self.assertEqual(result['searchMetadata']['instanceName'], self.core_name)

    def test_mdh_query_with_stopped_core_without_fallback_result_raises_connection_error(self) -> None:
        # Stop core beforehand
        mdh.cores.stop(self.core_name, keep=True)

        mdh_query = MDHQuery(self.core_name)

        self.assertRaises(ConnectionError, mdh_query.send_request_and_get_result, GRAPHQL_QUERY_PATH)

    def test_mdh_query_with_wrong_graphql_path_with_fallback_logs_exception_and_returns_result(self) -> None:
        # Save the result
        mdh_query = MDHQuery(self.core_name)
        result_orig = mdh_query.send_request_and_get_result(GRAPHQL_QUERY_PATH)

        with self.assertLogs(level='ERROR') as cm:
            result = mdh_query.send_request_and_get_result("Wrong graphql path")

        self.assertIn("FileNotFoundError", cm.output[0])
        self.assertEqual(result_orig, result)
        self.assertEqual(result['searchMetadata']['totalFilesCount'], 0)
        self.assertEqual(result['searchMetadata']['instanceName'], self.core_name)

    def test_mdh_query_with_wrong_graphql_path_without_fallback_raises_file_not_found_error(self) -> None:
        self.assertRaises(FileNotFoundError, MDHQuery(self.core_name).send_request_and_get_result, "Wrong graphql path")

    def test_mdh_query_with_wrong_graphql_syntax_with_fallback_logs_exception_and_returns_result(self) -> None:
        # Save the result
        mdh_query = MDHQuery(self.core_name)
        result_orig = mdh_query.send_request_and_get_result(GRAPHQL_QUERY_PATH)

        with self.assertLogs(level='ERROR') as cm:
            result = mdh_query.send_request_and_get_result(str(self.empty_graphql_query_path))

        self.assertIn("GraphQLSyntaxError", cm.output[0])
        self.assertEqual(result_orig, result)
        self.assertEqual(result['searchMetadata']['totalFilesCount'], 0)
        self.assertEqual(result['searchMetadata']['instanceName'], self.core_name)

    def test_mdh_query_with_wrong_graphql_syntax_without_fallback_raises_graphql_syntax_exception(self) -> None:
        self.assertRaises(GraphQLSyntaxError,
                          MDHQuery(self.core_name).send_request_and_get_result,
                          str(self.empty_graphql_query_path))