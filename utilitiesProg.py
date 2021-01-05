import configData
from os import walk
from os import listdir
from os import path
from os import rename
import yaml
from enum import Enum, unique
import pprint
import picture

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

@unique
class Status(Enum):
    OK = 0
    DATA_ERROR = 1
    NO_DATA = 2
    NOT_COMPLETE = 3
    NO_URL = 4

def checkGalleryStatus(fileName):
    galleryURL = "NO url!"
    try:
        data = configData.getCurrentData(fileName)
    except yaml.constructor.ConstructorError as error:
        print("DATA ERROR: " + fileName)
        print(error)
        return (Status.DATA_ERROR, fileName, galleryURL)
        

    if data is None:
        print("NO DATA: " + fileName)
        return (Status.NO_DATA, fileName, galleryURL)

    #wa  
    if ("dictitems" in data):  
        data = data.get("dictitems", data)
        pics = []
        picsDict = data.get('listOfPics', {})
        for pic in picsDict.values():
            a = picture.Picture(**pic)
            pics.append(a)

        data['listOfPics'] = pics

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)
        configData.dumpData(data, fileName)
        data = configData.GalleryData(**data)

    nbOfPics = data.getNbOfPics()
    nbTotalDownloaded = data.getNbTotalDownloaded()
    galleryURL = data.getGalleryURL()

    if (galleryURL.startswith("http") == False):
        print("NO_URL, {} of {}: {}".format(nbTotalDownloaded, nbOfPics, fileName) )

        return (Status.NO_URL, fileName, galleryURL)


    if (nbOfPics > nbTotalDownloaded):
        print("NOT COMPLETE, {} of {}: {}".format(nbTotalDownloaded, nbOfPics, fileName) )
        print(galleryURL)
        return (Status.NOT_COMPLETE, fileName, galleryURL) 

    return (Status.OK, fileName, galleryURL)
        

def checkAllGallerySatus():
    onlyDir = [f for f in listdir(dirPath) if path.isdir(path.join(dirPath, f))]

    results = []
    for dir in onlyDir:
        fileName = path.join(dirPath, dir)
        tuple = checkGalleryStatus(fileName)
        results.append(tuple)

    return results

import robot3
def completeGallerry(galStatuses):
    for gs in galStatuses:
        if (gs[0] is Status.NOT_COMPLETE):
            print("Status: " + str(gs[0]) + " dir: " + gs[1] )
            print("Gallery to complete: " + gs[2])
            robot3.mainGalleryGrabber(gs[2])

if __name__ == '__main__':
    results = checkAllGallerySatus()
    completeGallerry(results)
    
    #file = r"D:\media\xtreamdownloader\Beim FKK Wellness die Scheide vollnackt zeigen 3"
    #val = checkGalleryStatus(file)
    #print(val)
    