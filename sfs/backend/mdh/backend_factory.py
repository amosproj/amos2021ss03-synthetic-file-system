# 3rd party imports
import mdh

# Local imports
from sfs.backend import BackendFactory
from sfs.backend import BackendFactoryManager
from .backend import MDHBackend


class MDHBackendFactory(BackendFactory):
    """
    Implementation of the BackendFactory for the MDH.
    This Factory will create MDHBackends for given sections.
    See BackendFactory for more information
    """

    def __init__(self):
        super().__init__()
        try:
            mdh.init()
        except EnvironmentError:
            raise

    def create_backend_from_section(self, instance_cfg) -> MDHBackend:
        mdh_backend = MDHBackend(instance_cfg)
        return mdh_backend


# auto register backend
BackendFactoryManager().register_backend_factory(MDHBackendFactory(), 'mdh')
