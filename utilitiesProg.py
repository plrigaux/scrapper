import configData
from os import walk
from os import listdir
from os import path
from os import rename
import yaml
from enum import Enum

dirPath = configData.config["outputDirectory"]

def renameDataFile():
    f = []
    for (dirpath, dirnames, filenames) in walk(dirPath):
        print (dirpath)
        break

    onlyDir = [f for f in listdir(dirPath) if path.isdir(path.join(dirPath, f))]

    for dir in onlyDir:
        print (dir)
        fileName = path.join(dirPath, dir, "data.yaml")
        if (path.exists(fileName) == True):
            rename(fileName, path.join(dirPath, dir, configData.dataYaml))
            print("rename data to !data dir: " + dir)

class Status(Enum):
    OK = 0
    DATA_ERROR = 1
    NO_DATA = 2
    NOT_COMPLETE = 3

def checkGallerySatus():
    onlyDir = [f for f in listdir(dirPath) if path.isdir(path.join(dirPath, f))]

    results = []
    for dir in onlyDir:
        fileName = path.join(dirPath, dir)
        galleryURL = "NO url!"
        try:
            data = configData.getCurrentData(fileName)
        except yaml.constructor.ConstructorError:
            print("DATA ERROR: " + dir)
            results.append((Status.DATA_ERROR, dir, galleryURL))
            continue


        if data is None:
            print("NO DATA: " + dir)
            results.append((Status.NO_DATA, dir, galleryURL))
            continue

        nbOfPics = data.getNbOfPics()
        nbTotalDownloaded = data.getNbTotalDownloaded()
        galleryURL = data.getGalleryURL()

        if (nbOfPics > nbTotalDownloaded):
            print("NOT COMPLETE, {} of {}: {}".format(nbTotalDownloaded, nbOfPics, dir) )
            results.append((Status.NOT_COMPLETE, dir, galleryURL))
            print(galleryURL)
            
            continue

    return results

import robot3
def completeGallerry(galStatuses):
    for gs in galStatuses:
        if (gs[0] == Status.NOT_COMPLETE):
            print("Ge to complete: " + gs[2])
            robot3.mainGalleryGrabber(gs[2])

if __name__ == '__main__':
    res = checkGallerySatus()
    completeGallerry(res)
   