# Python imports
from importlib import import_module

# 3rd party imports
import toml

# Local imports
from sfs.paths import CONFIG_FILE_PATH
from sfs.backend import BackendFactoryManager
from sfs.backend import BackendManager
from sfs.errors import ConfigError


def _register_backend_factory(backend_name: str) -> None:
    """
    Registers a backend factory to the config parser
    :param backend_name: name of the backend (for example "mdh")
    :return: None
    """
    if backend_name not in SFSConfig.SUPPORTED_BACKENDS:
        raise ConfigError()
    module_name = f'sfs.backend.{backend_name}.backend_factory'
    import_module(module_name)


class SFSConfig:
    """
    Class that is responsible for parsing the config file.
    This class uses the given config file to create and initialize all the needed backends
    """

    SUPPORTED_BACKENDS = ['mdh', 'passthrough', 'fallback']

    def __init__(self, path=CONFIG_FILE_PATH):
        self.path = path
        self.settings = {}
        self.backend_configs = {}
        self._parse_config()

    def init(self):
        self._setup_backend_manager()

    @property
    def mountpoint(self):
        return self.settings.get('mountpoint')

    def _parse_config(self) -> None:
        """
        Parses the sfs config file and collects all the information about the backends that have to be
        created
        :return: None
        """
        # Current version works with toml file format
        with open(self.path, 'r') as fpointer:
            sfs_config = toml.load(fpointer)
        print(sfs_config)

        self.settings = sfs_config.pop('SETTINGS', None)

        sfs_config = {key.lower(): value for key, value in sfs_config.items()}
        # High level validation
        for key in sfs_config.keys():
            if key not in SFSConfig.SUPPORTED_BACKENDS:
                raise ConfigError(f"The current version of SFS does not support: {key}")

        # if only one instance of the backend is used include id: 1
        config_items = list(sfs_config.items())
        for backend_type, settings in config_items:
            # TODO: Create class for backend ids -> easier for large amount of backends
            if '1' not in settings:
                settings = {1: settings}
            sfs_config[backend_type] = settings
        print(sfs_config)
        self.backend_configs = sfs_config

    def _setup_backend_manager(self) -> None:
        """
        Creates all the needed backends, from the previously gathered information
        :return: None
        """
        backend_factory_manager = BackendFactoryManager()
        backend_heads = []
        for backend_name in self.backend_configs.keys():
            _register_backend_factory(backend_name)
            backend_factory = backend_factory_manager.get_factory_for_config_tag(backend_name)
            for instance_id, instance_cfg in self.backend_configs[backend_name].items():
                backend = backend_factory.create_backend_from_section(instance_cfg)
                backend_heads.append(backend.name)  # TODO
                BackendManager().add_backend(backend)
