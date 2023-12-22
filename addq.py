# Add a new gallery to the Tracker

import tracker
import urlqueue

def displayTraker():
    tracker.displayTraker()


def add_gallery():
    source_getter = urlqueue.SourceGetter()
    galleryURL = source_getter.getFirstValid(use_tracker=False)

    tracker.new_url(galleryURL)

if __name__ == '__main__':
    # main()
    add_gallery()