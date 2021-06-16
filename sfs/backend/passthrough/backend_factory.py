from sfs.backend import BackendFactory
from sfs.backend import BackendFactoryManager
from .backend import PassthroughBackend


class PassthroughBackendFactory(BackendFactory):
    """
    Implementation of the PassthroughBackend.
    This Factory will create PassthroughBackend for given sections.
    See PassthroughBackend for more information
    """

    def __init__(self):
        super().__init__()
        self.pt_id = 0

    def create_backend_from_section(self, instance_cfg) -> PassthroughBackend:
        self.pt_id += 1
        return PassthroughBackend(self.pt_id, instance_cfg)


# auto register backend
BackendFactoryManager().register_backend_factory(PassthroughBackendFactory(), 'passthrough')
