
from tkinter import Tk
import time
import os

import tracker 


class SourceGetter():

    def __init__(self):
        #self.queue = []
        self.last_clipboard = ''

    def checkUrl(self, url):

        galleryLink1 = 'www.imagefap.com/gallery.php?gid='
        galleryLink2 = 'www.imagefap.com/pictures/'
        galleryLink3 = 'www.imagefap.com/photo/'
        galleryLink4 = 'www.imagefap.com/gallery/'

        # check if url looks like a gallery url
        if (url.find(galleryLink1) != -1):
            return 1  # IF1
        elif (url.find(galleryLink2) != -1):
            return 2  # IF2
        elif (url.find(galleryLink3) != -1):
            return 3  # XH
        elif (url.find(galleryLink4) != -1):
            return 4  # IF3
        else:
            return 0

    def pollClipboard(self):
        # retrieve the current clipboard content
        try:
            clip = Tk()
            clip.withdraw()
            clipb = clip.clipboard_get()
            clip.destroy()
        except:
            clipb = ''
        return clipb

    def emptyClipboard(self):
        clip = Tk()
        clip.withdraw()
        clip.clipboard_clear()
        #clip.clipboard_append('i can has clipboardz?')
        clip.update()  # now it stays on the clipboard after the window is closed
        clip.destroy()

    def checkClipboard(self):
        # check if clipboard content has changed
        # check if the new content is a valid url and add to queue

        clipboard = self.pollClipboard()

        if (clipboard != self.last_clipboard):
            self.last_clipboard = clipboard
            urltype = self.checkUrl(clipboard)
            if urltype:
                print("OK URL: " + clipboard)
                #self.emptyClipboard()
                return clipboard

        return None

    def getFirstValid(self, use_tracker=True) -> str:

        if use_tracker:
            try:
                url = tracker.getFirstFailed()
                
                if url is None:
                    url = tracker.getFirstNew()

                if url is not None:
                    urltype = self.checkUrl(url)
                    if urltype:
                        print("OK URL FROM TRAKER" , url)
                        return url
                else :
                    print ("No url returned from tracker.")
            
            except Exception as exc:
                print("Tracker not working") 
                print(exc)   

        print("Copy (Ctrl-c) a valid url ...")
        while True:
            # fetch clipboard content and check for new url; add to queue if valid url is detected
            if url := self.checkClipboard():
                return url

                # check if queue contains a url
                #if len(urlqueue.queue): gallery.DownloadGallery()

            time.sleep(0.5)


if __name__ == "__main__":
    sg = SourceGetter()
    sg.getFirstValid()
