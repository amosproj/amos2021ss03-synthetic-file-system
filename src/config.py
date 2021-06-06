import BackendManager
from importlib import import_module
from BackendFactoryManager import BackendFactoryManager
from BackendManager import BackendManager
# import MDHBackendFactory  # this is not actually unused. This import triggers the auto registration of the factory
from paths import CONFIG_FILE_PATH2
import PassthroughBackendFactory
from typing import Dict
import toml


def _register_backend_factory(backend_name: str) -> None:
    factory_name = SFSConfig.BACKEND_FACTORIES[backend_name]
    import_module(factory_name)


class SFSConfig:

    SUPPORTED_BACKENDS = ['MDH', 'PT']
    BACKEND_FACTORIES = {
        'MDH': 'MDHBackendFactory',
        'PT': 'PassthroughBackendFactory'
    }

    @staticmethod
    def load_and_setup(path=None):
        return SFSConfig(path)

    def __init__(self, path=CONFIG_FILE_PATH2):
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

        # High level validation
        for key in sfs_config.keys()query:
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
        for backend_name in self.backend_configs.keys():
            _register_backend_factory(backend_name)
            backend_factory = backend_factory_manager.get_factory_for_config_tag(backend_name)
            for instance_id, instance_cfg in self.backend_configs[backend_name].items():

                print(instance_id)
                print(instance_cfg)
                if backend_name == 'MDH' and not instance_cfg.get("querySource", "") == 'file':
                    continue
                backend = backend_factory.create_backend_from_section(instance_cfg)
                BackendManager().add_backend(backend)
