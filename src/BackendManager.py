import logging

from singleton import singleton
from Backend import Backend
from MDHBackend import MDHBackend
from PassthroughBackend import PassthroughBackend


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

    def get_files_from_all_backends(self):
        files = []
        for backend in self.backends:
            source = 'unknown'
            if isinstance(backend, MDHBackend):
                source = 'MDH'
            if isinstance(backend, PassthroughBackend):
                source = 'PT'
            print(source)
            backend_files = (source, backend.get_all_files())
            #print(backend_files)
            files.append(backend_files)
        return files
