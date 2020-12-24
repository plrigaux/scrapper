

import re
from urllib.request import urlretrieve
import urllib.parse as urlparse
from urllib.parse import unquote

def main():

    gallery = 'https://www.imagefap.com/pictures/9157754/The-Simpson%27s-Merry-Christmas'

    gallery = unquote(gallery)
    parsed = urlparse.urlparse(gallery)

    print(parsed)
    print(parsed.path)
    print(parsed.path.rsplit('/', 1)[-1])

main()