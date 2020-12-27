import urllib.parse as urlparse
import re


def getGalleryName(gallery):
    gallery = urlparse.unquote(gallery)
    parsed = urlparse.urlparse(gallery)

    print(parsed)
    print(parsed.path)
    name = parsed.path.rsplit('/', 1)[-1]
    name = re.sub(r'[<>:"/\|?*]', '_', name)
    print("Gallery name: " + name)

    return name

def getCleanURL(url):
    return url.rsplit('?', 1)[0]