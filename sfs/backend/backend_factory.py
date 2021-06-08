import abc
from .backend import Backend


class BackendFactory:
    """
    Abstract parent class for every BackendFactory.
    BackendFactories are classes that, given a config section,
    create an instance of the Backend class, respective to the kind of factory
    (e.g. the MDHBackendFactory creates MDHBackend instances)
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def create_backend_from_section(self, section) -> Backend:
        """
        Abstract function. Subclasses of the BackendFactory have to implement this.
        The function should return an instance of Backend, configured for the given config section
        :param section: A toml table of a config file
        :return: An instance of the Backend class
        """
        pass
