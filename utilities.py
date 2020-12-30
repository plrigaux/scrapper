import urllib.parse as urlparse

import re


def getGalleryName(gallery) -> str:
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

def getNumber(alt) -> int:

    #m = re.search(r"(\d+)\s+of\s+(\d+)pics", alt)
    m = re.search(r"(\d+)\s+of\s+(\d+)\s+pics", alt)

    if m:
        return int(m.group(2))

    return -1

def urlSetParams(originalUrl, params) -> str:
    parsed = urlparse.urlparse(originalUrl)
    print(parsed)
    url_parts = list(parsed)
    print(url_parts)
    query = dict(urlparse.parse_qsl(url_parts[4]))
    print(query)
    query.update(params)
    print(query)

    url_parts[4] = urlparse.urlencode(query)
    print(url_parts)
    url = urlparse.urlunparse(url_parts)

    return url

def extractFileName(title) -> str:
    match = re.search(r'.*?\.\w+', title)

    if match:
        return match.group(0)
        
    return None    
