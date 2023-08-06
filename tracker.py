from nturl2path import url2pathname
from typing import Dict
from unicodedata import name
import yaml
import configData
from pathlib import Path
import os
import datetime
import configData
from pprint import pprint

TRACKER_FILE_NAME = "tracker.yaml"
FAILED = "FAILED"
IN_PROGRESS = "IN_PROGRESS"
NEW = "NEW"

galleries = {}


class TrackedGallery():

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                print("key", key)
                print("dictionary", dictionary)
                v = dictionary[key]
                setattr(key, v)

        for key in kwargs:
            setattr(self, key, kwargs[key])

    @property
    def date(self) -> str:
        return self.__dict__["date"]

    @property
    def url(self):
        return self.__dict__["url"]

    def __str__(self) -> str:
        #return __repr__()
        return str(self.__dict__)
    
    def __repr__(self) -> str:
        return str(self.__dict__)

    def __setattr__(self, name, value):
        self.__dict__[name] = value


"""
    def __iter__(self):
        return self.__dict__


    def __next__(self):
        return self.__dict__.__next__()

    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        if not name in self:
            raise AttributeError("Attribute {} does not exist".format(name))
        return self[name]
"""


def getTracker():
    pass


def saveTracker():
    pass


def getUncompletedGallery() -> str:
    pass


def save_a_process_gallery(gallery: configData.GalleryData, status=IN_PROGRESS) -> None:
    save_a_process(gallery.galleryName, gallery.galleryURL,
                   gallery.nbOfPics, gallery.nbTotalDownloaded, status)


def save_a_process(galleryName: str, galleryUrl: str, nbOfPics: int, nbTotalDownloaded: int, status=IN_PROGRESS) -> None:

    date = datetime.datetime.now().replace(microsecond=0).isoformat()
    proc = TrackedGallery(name=galleryName, url=galleryUrl,
                          date=date, nbOfPics=nbOfPics, nbTotalDownloaded=nbTotalDownloaded, status=status)
    load()
    galleries[proc.url] = proc
    save()


def in_progress(galleryData: configData.GalleryData):
    save_a_process_gallery(galleryData, status=IN_PROGRESS)

def failed(galleryData: configData.GalleryData):
    save_a_process_gallery(galleryData, status=FAILED)


def success(galleryData: configData.GalleryData):
    global galleries
    galleryData.status = "SUCCESS"
    load()
    # remove the tracking of sussessfull
    print("Gallery size B {}".format(len(galleries)))
    pprint(galleries)
    galleries.pop(galleryData.galleryURL, None)
    print("Gallery size A {}".format(len(galleries)))
    pprint(galleries, depth=3)

    save()


def save():
    global galleries
    data = []
    for gal in galleries.values():
        data.append(dict(gal.__dict__))

    data.sort(key=lambda x: x['date'], reverse=True)

    print("save data", len(data), "gallery lenght", len(galleries))
    print("save data", data)

    with open(tracker_file, mode="wt", encoding="utf-8") as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)


def getFirstFailed() -> str:
    return getFirst(FAILED)


def getFirstNew() -> str:
    return getFirst(NEW)



def getFirst(status) -> str:
    load()

    for track in [*galleries.values()]:
        if track.status == status:
            return track.url

    return None


def load():
    global galleries
    with open(tracker_file, 'r') as stream:
        data = yaml.load(stream, Loader=yaml.Loader)

    if data is None:
        print("No tracker loaded!", "Location: ", tracker_file)
        return

    data2 = []

    for tr in data:
        t = TrackedGallery(**tr)
        data2.append(t)

    #print(data2)

    data2.sort(key=lambda x: x.date, reverse=True)

    galleries = {i.url: i for i in data2}

    #print(galleries)


outDir = configData.getOutputDirectory()
tracker_file = os.path.join(outDir, TRACKER_FILE_NAME)
tracker_file_path = Path(tracker_file)
tracker_file_path.touch(exist_ok=True)

def displayTraker():
    load()
    print(yaml.dump(galleries, default_flow_style=False))
    print("Total galleries : ", len(galleries))
    nbOfPics = sum(int(p.nbOfPics) for p in galleries.values())
    print("Total pictures : ", nbOfPics)


def main():
    galleries = []
    t1 = TrackedGallery(**{"name": "ba", "url": "http"})

    print(t1.name)
    t1.name = "yoshi"
    t1.much = "yoshi"
    print(t1.name)
    print("t1", vars(t1))
    t2 = TrackedGallery(url="http://test.com nn", vache="cochon")
    #t3 =  TrackedGallery("name test new", "http://test.com 3436")
    #t1 =  { "name" :"a", "url" : "http"}
    #t2 =  { "name" :"name test", "url" : "http://test.com"}

    td1 = dict(t1.__dict__)
    print("td1", td1)
    print("t1", vars(t1))
    print("t2", vars(t2))
    #print ("t3", vars(t3))

    galleries.append(dict(t1.__dict__))
    galleries.append(td1)
    galleries.append(dict(t2.__dict__))
    # galleries.append(vars(t3))

    with open(tracker_file, mode="wt", encoding="utf-8") as file:
        yaml.dump(galleries, file, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    # main()
    displayTraker()
