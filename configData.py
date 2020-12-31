import yaml
import io
import os.path
from pathlib import Path

# Read YAML file
with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)


def getOutputDirectory(strPath):
    dirPath = os.path.join(config["outputDirectory"], strPath)
    return dirPath


def createAndGetOutputDirectory(strPath) -> str:
    dirPath = getOutputDirectory(strPath)
    Path(dirPath).mkdir(parents=True, exist_ok=True)

    return dirPath
