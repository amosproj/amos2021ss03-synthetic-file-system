import abc
import MDHBackend


class BackendFactory:

    def __init__(self):
        pass

    @abc.abstractmethod
    def create_backend_from_section(self, section):
        pass

