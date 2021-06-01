import logging

from singleton import singleton
from BackendFactory import BackendFactory


@singleton
class BackendFactoryManager:

    def __init__(self):
        self.factories: [(BackendFactory, str)] = []

    def register_backend_factory(self, factory: BackendFactory, section_tag: str):
        self.factories.append((factory, section_tag))

    def get_factory_for_config_tag(self, config_tag: str) -> BackendFactory:
        for (factory, tag) in self.factories:  # type: (BackendFactory, str)
            if tag == config_tag:
                return factory

        logging.error("Invalid tag name: " + config_tag)
