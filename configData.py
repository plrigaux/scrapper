import yaml
import re
import os.path
from pathlib import Path

# Read YAML file
with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)


def getOutputDirectory(strPath):
    strPath = re.sub(r'[<>:"/\|?*]', '_', strPath)
    dirPath = os.path.join(config["outputDirectory"], strPath)
    dirPath = os.path.normpath(dirPath)
    return dirPath


def createAndGetOutputDirectory(strPath) -> str:
    dirPath = getOutputDirectory(strPath)
    Path(dirPath).mkdir(parents=True, exist_ok=True)

    return dirPath

def dumpData(data, dirName):


    pictures = data.pop('listOfPics', [])

    newListOfPics = {}
    i = 1
    for pic in pictures:
        newListOfPics['pic_{:04d}'.format(i)] = vars(pic)
        i = i + 1

    data['listOfPics'] = newListOfPics
    
    outputFile = os.path.join(dirName, 'data.yaml')
    with open( outputFile, 'w') as file:
        documents = yaml.dump(data, file)
