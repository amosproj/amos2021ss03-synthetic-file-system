import BackendManager
from importlib import import_module
from BackendFactoryManager import BackendFactoryManager
from BackendManager import BackendManager
# import MDHBackendFactory  # this is not actually unused. This import triggers the auto registration of the factory
import PassthroughBackendFactory
from typing import Dict
import toml

"""
TEST FILE UNTIL THE PROPER CONFIG PARSER IS DONE!!!!
THIS FILE WILL BE REMOVED
"""


def test_setup():
    backfacman: BackendFactoryManager = BackendFactoryManager()
    backendfac = backfacman.get_factory_for_config_tag("MDH")
    backend = backendfac.create_backend_from_section(section="")
    BackendManager().add_backend(backend)


###  *** WIP ***

def _register_backend_factory(backend_name: str) -> None:
    factory_name = ConfigParser.BACKEND_FACTORIES[backend_name]
    import_module(factory_name)


class ConfigParser:

    SUPPORTED_BACKENDS = ['MDH', 'Passthrough']
    BACKEND_FACTORIES = {
        'MDH': 'MDHBackendFactory',
        'Passthrough': 'Passthrough'
    }

    @staticmethod
    def load_and_setup():
        return ConfigParser()

    def __init__(self, path='./config/config.cfg'):
        self.path = path
        self.sfs_config = self._parse_config()
        # sfs_config currently holds only backend relevant options
        # Might change within the next days
        self.backend_configs = self.sfs_config.copy()

    def init(self):
        self._setup_BackendManager()

    def _parse_config(self) -> Dict:
        # Current version works with toml file format
        with open(self.path, 'r') as fpointer:
            sfs_config = toml.load(fpointer)
        print(sfs_config)
        # High level validation
        for key in sfs_config.keys():
            if key not in ConfigParser.SUPPORTED_BACKENDS:
                raise NotImplementedError(f"The current version of SFS does not support: {key}")

        # if only one instance of the backend is used include id: 1
        config_items = list(sfs_config.items())
        for backend_type, settings in config_items:
            if '1' not in settings:
                settings = {1: settings}
            sfs_config[backend_type] = settings
        print(sfs_config)
        return sfs_config

    def _setup_BackendManager(self) -> None:
        backend_factory_manager = BackendFactoryManager()
        for backend_name in self.backend_configs.keys():
            _register_backend_factory(backend_name)
            backend_factory = backend_factory_manager.get_factory_for_config_tag(backend_name)
            for instance_id, instance_cfg in self.backend_configs[backend_name].items():
                print(instance_id)
                print(instance_cfg)
                backend = backend_factory.create_backend_from_section(instance_cfg)
                BackendManager().add_backend(backend)


if __name__ == '__main__':
    cfg_parser = ConfigParser('../config/config.cfg')
