# Python imports
import shutil
import time
import unittest
from contextlib import ExitStack
from pathlib import Path

# 3rd party imports
import json
import mdh
from mdh.types import MDHCore

# Local imports
from sfs.backend.mdh import MDHQueryRoot
from sfs.paths import GRAPHQL_QUERY_PATH


class TestBackendMDH(unittest.TestCase):

    file_path = None
    core_json_path = None
    cores_dir_path = None
    mdh_key = None
    mdh_key_lock = None
    core_name = None

    @classmethod
    def setUpClass(cls):
        # Setup needed paths
        cls.file_path = Path(__file__).parent
        cls.core_json_path = cls.file_path / "core.json"
        cls.cores_dir_path = cls.file_path / "cores"
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
        cls.mdh_key.unlink()
        cls.mdh_key_lock.unlink()

        mdh.cores.stop(cls.core_name)

    def setUp(self):
        with ExitStack() as stack:
            stack.callback(self.setUp)

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
        mdh_query = MDHQueryRoot(self.core_name, GRAPHQL_QUERY_PATH)
        result = mdh_query.send_request_get_result()

        self.assertEqual(result['searchMetadata']['totalFilesCount'], 0)
        self.assertEqual(result['searchMetadata']['instanceName'], self.core_name)

    def test_mdh_query_with_stopped_core_raises_connection_error(self) -> None:
        # Stop core beforehand
        mdh.cores.stop(self.core_name, keep=True)

        mdh_query = MDHQueryRoot(self.core_name, GRAPHQL_QUERY_PATH)

        self.assertRaises(ConnectionError, mdh_query.send_request_get_result)

    def test_mdh_query_with_wrong_graphql_path_raises_file_not_found_error(self) -> None:
        mdh_query = MDHQueryRoot(self.core_name, "Wrong graphql path")
        self.assertRaises(FileNotFoundError, mdh_query.send_request_get_result)
