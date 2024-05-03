import robot3
import configData
from os import walk
from os import listdir
from os import path
from os import rename
import yaml
from enum import Enum
import pprint
import picture
import json
import os
from datetime import datetime
from functools import total_ordering



dirPath = configData.config["outputDirectory"]


def renameDataFile():
    f = []
    for (dirpath, dirnames, filenames) in walk(dirPath):
        print(dirpath)
        break

    onlyDir = [f for f in listdir(
        dirPath) if path.isdir(path.join(dirPath, f))]

    for dir in onlyDir:
        print(dir)
        fileName = path.join(dirPath, dir, "data.yaml")
        if (path.exists(fileName) == True):
            rename(fileName, path.join(dirPath, dir, configData.dataYaml))
            print("rename data to !data dir: " + dir)


class Status(Enum):
    OK = 1
    DATA_ERROR = 2
    NO_DATA = 3
    NOT_COMPLETE = 4
    NO_URL = 5
    MALFORMED = 6

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def toJSON(self):
        return self.name

@total_ordering
class GalleryAssesement:
    def __init__(self, status: Status, file_name: str, url: str, mdate=None, details=None) -> None:
        self.status = status
        self.data_register_file = file_name
        self.url = url
        self.mdate = mdate
        self.details = details


def checkGalleryStatus(fileName: str) -> GalleryAssesement:
    galleryURL = "NO url!"
    mdate = None
    try:
        data = configData.getCurrentData(fileName)
    except yaml.constructor.ConstructorError as error:
        print("DATA ERROR: " + fileName)
        print(error)
        return GalleryAssesement(Status.DATA_ERROR, fileName, galleryURL, mdate)
    except Exception as e:
        print("MALFORMED: " + fileName)
        print("Exception raised", e)
        return GalleryAssesement(Status.NO_DATA, fileName, galleryURL, mdate)

    mdate_float = os.path.getmtime(fileName)
    mdate = datetime.fromtimestamp(mdate_float).strftime('%Y-%m-%d')

    if data is None:
        print("NO DATA: " + fileName)
        return GalleryAssesement(Status.NO_DATA, fileName, galleryURL, mdate)

    # wa
    if (hasattr(data, "dictitems")):
        data = data.get("dictitems", data)
        pics = []
        picsDict = data.get('listOfPics', {})
        for pic in picsDict.values():
            a = picture.Picture(**pic)
            pics.append(a)

        data['listOfPics'] = pics

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)
        configData.dumpData(data)
        data = configData.GalleryData(**data)

    nbOfPics = data.nbOfPics
    nbTotalDownloaded = data.nbTotalDownloaded
    galleryURL = data.galleryURL

    if (galleryURL is None or galleryURL.startswith("http") == False):
        print("NO_URL, {} of {}: {}".format(
            nbTotalDownloaded, nbOfPics, fileName))

        return GalleryAssesement(Status.NO_URL, fileName, galleryURL, mdate)

    if (nbOfPics > nbTotalDownloaded):
        details = f"{nbTotalDownloaded} of {nbOfPics}"
        print("NOT COMPLETE, {}: {}".format(
            details, fileName))
        print(galleryURL)
        return GalleryAssesement(Status.NOT_COMPLETE, fileName, galleryURL, mdate, details)

    return GalleryAssesement(Status.OK, fileName, galleryURL, mdate)


def checkAllGallerySatus() -> list[GalleryAssesement]:
    onlyDir = [f for f in listdir(
        dirPath) if path.isdir(path.join(dirPath, f))]

    results: list[GalleryAssesement] = []

    for dir in onlyDir:
        fileName = path.join(dirPath, dir)
        res = checkGalleryStatus(fileName)
        results.append(res)

    return results


def completeGallerry(galStatuses):
    for gs in galStatuses:
        if (gs[0] is Status.NOT_COMPLETE):
            print("Status: " + str(gs[0]) + " dir: " + gs[1])
            print("Gallery to complete: " + gs[2])
            robot3.mainGalleryGrabber(gs[2])

DUMP_FILE_NAME = "gallery_results.json"

def json_dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


if __name__ == '__main__':
    # load_results()

    results = checkAllGallerySatus()

    """     ga1 = GalleryAssesement(Status.MALFORMED, "/home", "http://", "1909-01-32")

    ga2 = GalleryAssesement(Status.NO_URL, "/home", None, "1900-04-32")


    results = [ga1, ga2] """

    results.sort(key=lambda x: (x.status, x.mdate if x.mdate is not None else ""))

    json_string = json.dumps(
        [ob.__dict__ for ob in results], indent=4, sort_keys=False, default=json_dumper)
    with open(DUMP_FILE_NAME, 'w') as gallery_results_file:
        gallery_results_file.write(json_string)

    # completeGallerry(results)

    # file = r"D:\media\xtreamdownloader\Beim FKK Wellness die Scheide vollnackt zeigen 3"
    # val = checkGalleryStatus(file)
    # print(val)
