from BackendFactory import BackendFactory
from MDHBackend import MDHBackend
from BackendFactoryManager import BackendFactoryManager
from mdh_bridge import *

import fuse_utils
import paths
import mdh

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
            # TODO: Error handling
        except Exception:
            raise EnvironmentError
        #self.core_name = "core-test"  # TODO read from section

    def create_backend_from_section(self, instance_cfg) -> MDHBackend:
        core_name = instance_cfg['core']
        print('*'*80)
        print(instance_cfg)
        # Setting up the config for the Backend
        mdh_backend = MDHBackend(instance_cfg)
        return mdh_backend


# auto register backend
BackendFactoryManager().register_backend_factory(MDHBackendFactory(), "MDH")
