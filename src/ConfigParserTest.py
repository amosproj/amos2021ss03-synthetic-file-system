import BackendManager
from BackendFactoryManager import BackendFactoryManager
from BackendFactory import BackendFactory
from BackendManager import BackendManager
import MDHBackendFactory


def test_setup():
    backfacman: BackendFactoryManager = BackendFactoryManager()
    backendfac = backfacman.get_factory_for_config_tag("MDH")
    backend = backendfac.create_backend_from_section(section="")
    BackendManager().add_backend(backend)

