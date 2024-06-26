from nturl2path import url2pathname
from configData import GalleryData
import yaml
import configData
from pathlib import Path
import os
import datetime
from pprint import pprint

from common import *
TRACKER_FILE_NAME = "tracker.yaml"


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
    
    def status(self) -> str:
        return self.__dict__["status"]


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


def save_a_process_gallery(gallery: configData.GalleryData, status=IN_PROGRESS, old_gallery_url=None ) -> None:
    save_a_process(gallery.galleryName, gallery.galleryURL,
                   gallery.nbOfPics, gallery.nbTotalDownloaded, status, old_gallery_url )


def save_a_process(galleryName: str, galleryUrl: str, nbOfPics: int, nbTotalDownloaded: int, status=IN_PROGRESS, old_gallery_url:str=None ) -> None:

    date = datetime.datetime.now().replace(microsecond=0).isoformat()
    proc = TrackedGallery(name=galleryName, url=galleryUrl,
                          date=date, nbOfPics=nbOfPics, nbTotalDownloaded=nbTotalDownloaded, status=status)
    load()
    galleries[proc.url] = proc

    if proc.url != old_gallery_url :
        galleries.pop(old_gallery_url, None)

    save()


def in_progress(galleryData: configData.GalleryData, old_gallery_url : str):
    save_a_process_gallery(galleryData, status=IN_PROGRESS, old_gallery_url=old_gallery_url)

def failed(galleryData: configData.GalleryData):
    save_a_process_gallery(galleryData, status=FAILED)

def invalid_gallery_url(galleryData: GalleryData):
    save_a_process_gallery(galleryData, status=INVALID_GALLERY_URL)

def new_url(url: str):
    gallery = GalleryData(url)

    save_a_process_gallery(gallery, status=NEW)

def success(galleryData: configData.GalleryData):
   
    galleryData.status = SUCCESS
    load()
    # remove the tracking of sussessfull
    print("Gallery size B {}".format(len(galleries)))
    pprint(galleries)
    galleries.pop(galleryData.galleryURL, None)
    print("Gallery size A {}".format(len(galleries)))
    pprint(galleries, depth=3)

    save()


def save():

    data = []
    for gal in galleries.values():
        data.append(dict(gal.__dict__))

    data.sort(key=lambda x: x['date'], reverse=True)

    with open(tracker_file, mode="wt", encoding="utf-8") as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)

    print_tracked_info()


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

    print("TRACKER FILE:", Path(tracker_file).absolute())
    
    #Create if doesnt exist
    Path(tracker_file).touch(exist_ok=True)

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

def displayTraker():
    load()
    print_tracked_info()

def galleries_filter(pair: tuple[str, TrackedGallery]) -> bool:

    key, value  = pair

    if value.status == "FAILED2":
        return False

    return True

def print_tracked_info():

    filtered_galleries = dict(filter(galleries_filter, galleries.items()))

    dumb = yaml.dump(filtered_galleries, default_flow_style=False)
    print(dumb)
    print("Tracked Total galleries : ", len(galleries))
    nbOfPics = sum(int(p.nbOfPics) for p in galleries.values())
    print("Tracked Total pictures : ", nbOfPics)

    
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
    #new_url("https://www.imagefap.com/gallery/10257503")
