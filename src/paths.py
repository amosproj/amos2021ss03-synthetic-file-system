# Python imports
import os

# Directory paths
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CONFIG_PATH = os.path.join(ROOT_PATH, "config")

# File paths
CONFIG_FILE_PATH = os.path.join(CONFIG_PATH, "config.graphql")
