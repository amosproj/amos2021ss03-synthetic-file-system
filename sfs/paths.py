# Python imports
from pathlib import Path

# Directory paths
ROOT_PATH = Path(__file__).parent.parent
CONFIG_PATH = ROOT_PATH / "config"

# File paths
GRAPHQL_QUERY_PATH = CONFIG_PATH / "config.graphql"
CONFIG_FILE_PATH = CONFIG_PATH / "config.cfg"
