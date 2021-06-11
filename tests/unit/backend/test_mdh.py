# Python imports
import unittest
import shutil
from contextlib import ExitStack
from pathlib import Path

# 3rd party imports
import mdh
import json

# Local imports
# from sfs.paths import GRAPHQL_QUERY_PATH


class TestBackendMDH(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup needed paths
        file_path = Path(__file__).parent
        cls.core_json_path = file_path / "core.json"
        cls.cores_dir_path = file_path / "cores"
        cls.mdh_key = file_path / ".mdh"

        # Setup json file for a mdh core
        core_json = {
            "name": "core-test",
            "version": "latest",
            "passwords": {
                "user": "user",
                "admin": "admin"
            },
            "directories": {
                str(file_path): "Test"
            },
            "port": 11000,
            "database": "mdh-core-test-db"
        }
        with open(cls.core_json_path, 'w') as f:
            json.dump(core_json, f)

        # Setup environment and core
        with ExitStack() as stack:
            stack.callback(cls.tearDownClass)

            mdh.init(file_path)

            stack.pop_all()

    @classmethod
    def tearDownClass(cls):
        cls.core_json_path.unlink()
        cls.mdh_key.unlink()
        shutil.rmtree(cls.cores_dir_path)
