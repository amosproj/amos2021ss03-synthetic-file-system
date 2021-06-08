import logging

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

    def get_file_paths(self, backends=None):
        if backends is None:
            backends = self.backends
        file_paths = []
        for backend in backends:
            if isinstance(backend, MDHBackend):
                source = 'mdh'
            if isinstance(backend, PassthroughBackend):
                source = 'passthrough'
            file_paths.append((source, backend.get_file_paths()))
        return file_paths
