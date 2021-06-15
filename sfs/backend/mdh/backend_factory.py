# 3rd party imports
import mdh

# Local imports
import sfs.paths
from sfs.backend import BackendFactory
from sfs.backend import BackendFactoryManager
from .backend import MDHBackend
from .query import MDHQueryRoot


class MDHBackendFactory(BackendFactory):
    """
    Implementation of the BackendFactory for the MDH.
    This Factory will create MDHBackends for given sections.
    See BackendFactory for more information
    """

    def __init__(self):
        super().__init__()
        self.count = 0
        try:
            mdh.init()
            # TODO: Error handling
        except Exception:
            raise EnvironmentError

    def create_backend_from_section(self, instance_cfg) -> MDHBackend:
        self.count += 1
        return MDHBackend(self.count, instance_cfg)

# auto register backend
BackendFactoryManager().register_backend_factory(MDHBackendFactory(), 'mdh')
