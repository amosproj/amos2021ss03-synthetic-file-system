# 3rd party imports
import toml
from typing import Dict
from importlib import import_module

# Local imports
from sfs.paths import CONFIG_FILE_PATH
from sfs.backend import BackendFactoryManager
from sfs.backend import BackendManager
# import MDHBackendFactory  # this is not actually unused. This import triggers the auto registration of the factory


def _register_backend_factory(backend_name: str) -> None:
    if backend_name not in SFSConfig.SUPPORTED_BACKENDS:
        raise NotImplementedError()
    module_name = f'sfs.backend.{backend_name}.backend_factory'
    import_module(module_name)


class SFSConfig:

    SUPPORTED_BACKENDS = ['mdh', 'passthrough']

    @staticmethod
    def load_and_setup(path=None):
        return SFSConfig(path)

    def __init__(self, path=CONFIG_FILE_PATH):
        self.path = path
        self.settings = {}
        self.backend_configs = {}
        self._parse_config()

    def init(self):
        self._setup_BackendManager()

    def _parse_config(self) -> None:
        # Current version works with toml file format
        with open(self.path, 'r') as fpointer:
            sfs_config = toml.load(fpointer)
        print(sfs_config)

        self.settings = sfs_config.pop('SETTINGS', None)

        sfs_config = {key.lower(): value for key, value in sfs_config.items()}
        # High level validation
        for key in sfs_config.keys():
            if key not in SFSConfig.SUPPORTED_BACKENDS:
                raise NotImplementedError(f"The current version of SFS does not support: {key}")

        # if only one instance of the backend is used include id: 1
        config_items = list(sfs_config.items())
        for backend_type, settings in config_items:
            # TODO: Create class for backend ids -> easier for large amount of backends
            if '1' not in settings:
                settings = {1: settings}
            sfs_config[backend_type] = settings
        print(sfs_config)
        self.backend_configs = sfs_config

    def _setup_BackendManager(self) -> None:
        backend_factory_manager = BackendFactoryManager()
        for factory in backend_factory_manager.factories:
            print(factory)

        for backend_name in self.backend_configs.keys():
            _register_backend_factory(backend_name)
            backend_factory = backend_factory_manager.get_factory_for_config_tag(backend_name)
            print(backend_name)
            print(backend_factory)
            for instance_id, instance_cfg in self.backend_configs[backend_name].items():

                print(instance_id)
                print(instance_cfg)
                if backend_name == 'mdh' and not instance_cfg.get("querySource", "") == 'file':
                    continue
                backend = backend_factory.create_backend_from_section(instance_cfg)
                BackendManager().add_backend(backend)
