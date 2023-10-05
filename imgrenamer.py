import sys
import time
from os import path
import os
import shutil
from optparse import OptionParser
from PIL import Image
import ffmpeg
from pprint import pprint # for printing Python dictionaries in a human-readable way
import traceback

def main():
    #optParser = OptionParser("usage: %prog [options] images... ")
    #optParser.add_option("-p","--prefix",help="New File Prefix Date Format",action="store",type="string",dest="dateFormat", default="%Y-%m-%d_")
    #optParser.add_option("-d","--dry",help="Only show the rename, NO MOVE WILL BE PERFORMED",action="store_true",dest='dry')
    #(options,args) = optParser.parse_args(sys.argv)
    dateFormat = '%Y%m%d_%H%M%S'

    dry = False

    folder = '/home/plr/Pictures/recovery/recup_dir.1'
    files = os.listdir(folder)

    for imagePath in files:
        imgfullpath = os.path.join(folder, imagePath)
        base_filename, file_extension = os.path.splitext(imagePath)
        try:

            if file_extension == ".mp4":
                meta = ffmpeg.probe(imgfullpath)["streams"]
                #pprint(meta)
                print(imgfullpath)

                strImageDate = meta[0]['tags']['creation_time']
                imageDate = time.strptime(strImageDate, "%Y-%m-%dT%H:%M:%S.%fZ")
                print("Date", strImageDate)

            else:
                continue
                img = Image.open(imgfullpath)
                exif_data = img._getexif()
                strImageDate = exif_data[306]
                imageDate = time.strptime(strImageDate, "%Y:%m:%d %H:%M:%S")
            
            
            newFileName = time.strftime(dateFormat, imageDate)
            
            


            newPath = path.join(folder,"..",newFileName + file_extension)
            if dry:
                print(imagePath + " -> "+newPath)
            else:
                shutil.move(imgfullpath, newPath)
        except IOError as e:
            print("File " + imagePath + " not found", e)
        except TypeError as te:
            print("No EXIF date Information found for file: " + imgfullpath)
            traceback.print_exc()
        except Exception as e:
            print (e)
            traceback.print_exc()

            

if __name__ == '__main__':
    main()
