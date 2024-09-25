import yaml
import re
import os.path

from pathlib import Path
import picture
#from pprint import pprint
import pprint
from picture import Picture
from common import *

DATAYAML_FILE_NAME = '!data.yaml'


class GalleryData(object):
    galleryURL: str = None
    nbOfPics: int = -1
    galleryName: str = UNKNOWN
    nbTotalDownloaded = -1
    listOfPics: list[Picture] = []
    categories: list[str] = []


    def __init__(self, galleryURL=None, galleryName = UNKNOWN):
        self.galleryURL = galleryURL
        self.galleryName = galleryName


    def has_name(self) -> bool:
        return self.galleryName is not None
    
    def __repr__(self) -> str:
        #print("!!!!!!!!!!!!!!!!!!!!!", self.__dict__.keys())
        to_out_str = {}
        your_blacklisted_set = ["listOfPics"]
        for key, value in self.__dict__.items():
            if key not in your_blacklisted_set:
                to_out_str[key] = value
        
        return str(to_out_str)


"""
    def __getattr__(self, name):
        # if not self.has_key(name):
        #    raise AttributeError(
        #        "Attribute \"{}\" does not exist. Here possible choices: {}".format(name, self.keys()))
        return self[name]

    def __setattr__(self, name, value):
        self[name] = self.string_empty_to_none(value)

    def __delattr__(self, name):
        if not name in self:
            raise AttributeError(
                "Attribute \"{}\" does not exist".format(name))
        del self[name]

    def string_empty_to_none(self, value):
        if (type(value) != str):
            return value

        if (len(value) == 0):
            return None

        return value

"""


try:
    # Read YAML file
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
except:
    # Read YAML file
    with open("../config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

def from_dict(data: dict) ->GalleryData: 
    gallery = GalleryData()

    for key, value in data.items(): 
        gallery.__dict__[key] = value

    pics = []

    list_picture_map = data["listOfPics"]

    for pic in list_picture_map.values():
        a = picture.Picture(**pic)
        pics.append(a)

    gallery.listOfPics = pics

    return gallery



def getOutputDirectory(strPath="") -> str:

    root_dir_list = config["collectionDirectories"]
    default_dir = config["outputDirectory"]

    if strPath:
        strPath = re.sub(r'[<>:"/\|?*]', '_', strPath)

        # give the collection path first
        for root_dir in root_dir_list:
            dirPath = os.path.join(root_dir, strPath)
            dirPath = os.path.normpath(dirPath)

            my_file = Path(dirPath)
            if my_file.is_dir():

                # ensure that the dir has a data file
                fileName = os.path.join(my_file, DATAYAML_FILE_NAME)
                data_file = Path(fileName)
                if data_file.is_file():
                    return dirPath

    dirPath = os.path.join(default_dir, strPath)
    dirPath = os.path.normpath(dirPath)
    return dirPath


def createAndGetOutputDirectory(strPath: str) -> str:
    dirPath = getOutputDirectory(strPath)
    Path(dirPath).mkdir(parents=True, exist_ok=True)

    return dirPath


def dumpData(gallery: GalleryData):

    dirName = createAndGetOutputDirectory(gallery.galleryName)

    print("Dump data tracker to :", dirName)
    data = vars(gallery)
    oldPictures = data.pop('listOfPics', [])

    newListOfPics = {}
    nbPictures = len(oldPictures)

    if nbPictures == 0:
        print("Don't dump gallery empty")
        return

    picStr = generatePicStr(nbPictures)

    i = 1
    for pic in oldPictures:
        try:
            newListOfPics[picStr.format(i)] = vars(pic)
            i = i + 1
        except TypeError:
            print("TypeError pic: " + str(pic))
            print("TypeError pic: " + str(type(pic)))
            raise

    data['listOfPics'] = newListOfPics

    outputFile = os.path.join(dirName, DATAYAML_FILE_NAME)
    with open(outputFile, 'w') as file:
        yaml.dump(
            data, file,  default_flow_style=False, sort_keys=False)

    data['listOfPics'] = oldPictures


def generatePicStr(nbPictures):
    zeroPad = len(str(nbPictures))
    # print('{} {}'.format(nbPictures, zeroPad))

    picStr = 'pic_{:0' + str(zeroPad) + 'd}'
    return picStr


def updateList(data: GalleryData, listOfPics):

    currentList = data.listOfPics

    if not currentList:
        data.listOfPics = listOfPics

    else:

        for picCurr, picScraped, i, j in zip(currentList, listOfPics, range(len(currentList)), range(len(listOfPics))):
            pass

        for picScraped in listOfPics[len(currentList):]:
            currentList.append(picScraped)


"""
def test1():
        d = {'zname': 'Silenthand Olleander', 'race': 'Human', "b" : 'h',
            'traits': ['ONE_HAND', 'ONE_EYE']}
        d['a'] = "pata"
        s = yaml.dump(d, default_flow_style=False, sort_keys=False)
        print(s)

        s = yaml.dump(d)
        print(s)
        d = collections.OrderedDict()

        d['zname'] = 'Silenthand Olleander'
        d['race'] = 'Human'
        d['traits'] = ['ONE_HAND', 'ONE_EYE']

        yaml.add_representer(collections.OrderedDict, lambda dumper,
                            data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))

        s = yaml.dump(d)
        print(s)


            p = picture.Picture("a", "b", "c")
    print(p)

    s = yaml.dump(p)
    print(s)

    o = yaml.load(s, Loader=yaml.FullLoader)
    print(type(o))
    print(o)
"""


def loadGalleryData(loader, node):
    print("______________________________")
    # print(loader)
    print(type(node))
    print("______________________________")
    fields = loader.construct_mapping(node)
    g = GalleryData(**fields)
    return g


def getCurrentData(directory: str) -> GalleryData:
    fileName = os.path.join(directory, DATAYAML_FILE_NAME)
    fileName = os.path.normpath(fileName)

    if (os.path.exists(fileName) == False):
        print("file doesn't exists: ", fileName)
        return None

    yaml.add_constructor(
        "tag:yaml.org,2002:python/object/new:configData.GalleryData", loadGalleryData)
    with open(fileName, 'r') as stream:
        data = yaml.load(stream, Loader=yaml.Loader)

    try:
        gallery = from_dict(data)
    except Exception as e:
        print("FAIL to load gallery from ", fileName)
        raise e


    #print_gallery(gallery)
    return gallery

def print_gallery(gallery :GalleryData):
     #data = vars(gallery)
     #pretty_json = json.dumps(data, indent=4)
     #print(pretty_json)
     if gallery is None:
         print("Gallery is None!")
         return
     
     pprint.pprint(vars(gallery), depth=6, sort_dicts=False)

if __name__ == "__main__":
    print("tests")
    directory = r"/mnt/samdata/media/xtreamdownloader/With painted nails, and a shaved muff_ she's ready for the wolf"
    directory = r"/mnt/samdata/media/xtreamdownloader/StarWars Hors Wookie Sex"

    data = getCurrentData(directory)

    print_gallery(data)
