import logging

from singleton import singleton
from Backend import Backend


@singleton
class BackendManager:

    def __init__(self):
        self.backends: [Backend] = []

    def add_backend(self, backend: Backend):
        self.backends.append(backend)

    def get_backend_for_path(self, path: str) -> Backend:
        for backend in self.backends:
            if backend.contains_path(path):
                return backend
        logging.error("There is no backend responsible for this path!")
