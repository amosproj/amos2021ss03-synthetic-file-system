# 3rd party imports
import logging

# Local imports
from sfs.singleton import singleton
from .backend_factory import BackendFactory


@singleton
class BackendFactoryManager:
    """
    Manager for the BackendFactories. It is used by the ConfigParser to retrieve the correct factories
    for every part in the config file
    """

    def __init__(self):
        """
        Constructor; just initializes the factories list.
        This list holds pairs of BackendFactories and their respective section name, e.g.
        (MDHBackendFactory, "mdh")
        """
        self.factories: [(BackendFactory, str)] = []

    def register_backend_factory(self, factory: BackendFactory, section_tag: str):
        """
        Registers a factory to the Manager
        :param factory: Instance of the factory
        :param section_tag: tag of the section name that this factory accepts
        :return: None
        """
        self.factories.append((factory, section_tag))

    def get_factory_for_config_tag(self, config_tag: str) -> BackendFactory:
        """
        Returns a factory for a given section tag from the list of internally registers factories
        :param config_tag: The section tag
        :return: The correct factory for the given tag
        """
        for (factory, tag) in self.factories:  # type: (BackendFactory, str)
            if tag == config_tag:
                return factory

        logging.error("Invalid tag name: " + config_tag)

