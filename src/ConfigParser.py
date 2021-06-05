import BackendManager
from importlib import import_module
from BackendFactoryManager import BackendFactoryManager
from BackendManager import BackendManager
#import MDHBackendFactory  # this is not actually unused. This import triggers the auto registration of the factory
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

class ConfigParser:
    SUPPORTED_BACKENDS = ['MDH', 'Passthrough']
    BACKEND_FACTORIES = {
        'MDH': 'MDHBackendFactory',
        'Passthrough': 'Passthrough'
    }

    def __init__(self, path='./config/config.cfg'):
        self.path = path
        self.sfs_config = self._load_config()
        self._validate()
        self.backend_configs = {}
        self._setup_backend_configs()
        self._register_backend_factories()
        self._setup_BackendManger()

    def _load_config(self) -> Dict:
        # Current version works with toml file format
        with open(self.path, 'r') as fpointer:
            sfs_config = toml.load(fpointer)
        print(sfs_config)
        return sfs_config

    def _validate(self):
        # High level validation of the basic structure
        # backend specific validation needs to be done individually
        for key in self.sfs_config.keys():
            if key not in ConfigParser.SUPPORTED_BACKENDS:
                raise NotImplementedError(f"The current version of SFS does not support: {key}")

    def _setup_backend_configs(self):
        for entry in self.sfs_config:
            print(entry)
        for system in SFSConfigManager.supported_configs:
            pass
            #if system in config_repr:
                #constructor = SFSConfigManager.supported_configs[system]
                #args = config_repr[system]
                #self.configs[system] = constructor(args)

    def _register_backend_factories(self):
        for system in self.configs.keys():
            factory_name = ConfigParser.BACKEND_FACTORIES[system]
            import_module(factory_name)

    def _setup_BackendManager(self):
        backend_factory_manager = BackendFactoryManager()
        for backend_name in self.configs.keys():
            backend_factory = backend_factory_manager.get_factory_for_config_tag(backend_name)
            for config in self.configs[backend_name]:
                backend = backend_factory.create_backend_from_section(config)
                BackendManager().add_backend(backend)


if __name__ == '__main__':
    cfg_parser = ConfigParser('../config/config.cfg')
