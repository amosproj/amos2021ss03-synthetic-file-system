# 3rd party imports
import logging

# Local imports
from sfs.singleton import singleton
from .backend import Backend
from .mdh import MDHBackend
from .passthrough import PassthroughBackend


@singleton
class BackendManager:
    """
    Manager class for the backends. The SFS will retrieve the backend that is needed for some
    call from this manager.
    """
    def __init__(self):
        self.backends: [Backend] = []

    def add_backend(self, backend: Backend):
        """
        Registers a backend to the Manager
        :param backend: The Backend that is to be registered
        :return: None
        """
        self.backends.append(backend)

    def get_backend_for_path(self, path: str) -> Backend:
        """
        Retrieves the Backend that is responsible for dealing with a certain path from the list of internally
        registered backends
        :param path: The path to a file for which the responsible backend is retrieved
        :return: The backend responsible for the given file or None if there is no Backend that fits
        """
        for backend in self.backends:
            if backend.contains_path(path):
                return backend
        logging.error("There is no backend responsible for this path!")

    def get_backend_by_name(self, name: str) -> Backend:
        """
        Retrieves the Backend with the given name.
        :param name: The name of the requested backend.
        :return: The backend with the given name.
        """
        for backend in self.backends:
            if backend.name == name:
                return backend
        return None

    def get_file_paths(self, target_backends=None):
        if target_backends is None:
            target_backends = self.backends
        file_paths = []
        for backend in target_backends:
            file_paths.append((backend.name, backend.get_file_paths()))
        return file_paths
