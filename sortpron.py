import os
import shutil

# Get the list of all files and directories
path = "/media/plr/DATA/media/img/"
dir_list = os.listdir(path)
 
print("Files and directories in '", path, "' :")
 
# prints all files
print(dir_list)


pathd = "/media/plr/DATA/media/img/Uncat/"


for file in dir_list:
    print(len(file),file)
    if (len(file) > 13):
        origin = path + file
        dest = pathd + file
        shutil.move(origin, dest)