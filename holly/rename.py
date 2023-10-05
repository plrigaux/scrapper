
from os import listdir
from os.path import isfile, join
import re

mypath = "/media/plr/DATA/media/img/Nude in public/Cruise Anna.M Nikola.P/"


def main():
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    onlyfiles.sort()

    p = re.compile("nikop-nv-(\d+)(.+)")
    for file in onlyfiles:

        m = p.match(file)
        if m:
            print(file, m.group(1))
        else:
            print(file)


if __name__ == '__main__':
    main()