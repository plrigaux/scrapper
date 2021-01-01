import yaml
import re
import os.path
import collections
from pathlib import Path
import picture

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

    oldPictures = data.pop('listOfPics', [])

    newListOfPics = {}
    nbPictures = len(oldPictures)
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

    outputFile = os.path.join(dirName, 'data.yaml')
    with open(outputFile, 'w') as file:
        yaml.dump(
            data, file,  default_flow_style=False, sort_keys=False)

    data['listOfPics'] = oldPictures


def generatePicStr(nbPictures):
    zeroPad = len(str(nbPictures))
    #print('{} {}'.format(nbPictures, zeroPad))

    picStr = 'pic_{:0' + str(zeroPad) + 'd}'
    return picStr


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

def getCurrentData(directory) -> dict:
    fileName = os.path.join(directory, 'data.yaml')
    fileName = os.path.normpath(fileName)
    
    if (os.path.exists(fileName) == False):
        print ("file doesn't exists: " + fileName)
        return None
    
    with open(fileName, 'r') as stream:
        data = yaml.safe_load(stream)

    picsDict = data.get('listOfPics', {})

    pics = []
    for pic in picsDict.values():
        a = picture.Picture(**pic)
        pics.append(a)

    data['listOfPics'] = pics

    return data

if __name__ == "__main__":
    print("tests")
    directory = r"D:\media\xtreamdownloader\Cali Carter - Workout Slut" 

    data = getCurrentData(directory)
    


    #print(data)

    l = data['listOfPics']

    for i, val in enumerate(l, start = 100):
        print(i, val)