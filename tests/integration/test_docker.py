# Python imports
import unittest
from subprocess import run, DEVNULL

# 3rd party imports
import docker
import yaml
from docker.errors import NotFound

# Local imports
from sfs.paths import ROOT_PATH


class TestIntegratedTool(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.DOCKER_YML = ROOT_PATH / "docker-compose.yml"

        with open(cls.DOCKER_YML, 'r') as stream:
            try:
                container_spec = yaml.safe_load(stream)['services']['synthetic-file-system']
            except yaml.YAMLError:
                raise
        container_name = container_spec['container_name']
        cls.image_name = container_spec['image']

        run(["docker-compose", "up", "-d", "--build"], stdout=DEVNULL)

        cls.client = docker.from_env()

        try:
            cls.container = cls.client.containers.get(container_name)
        except NotFound:
            raise

    @classmethod
    def tearDownClass(cls):
        run(["docker-compose", "down"], stdout=DEVNULL)

        cls.client.images.remove(cls.image_name)
