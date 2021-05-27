from pathlib import Path
from sys import path

ROOT_PATH = Path(__file__).parent.parent
SOURCE_PATH = ROOT_PATH / "src"

path.append(SOURCE_PATH)