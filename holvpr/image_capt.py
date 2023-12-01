import json
from pathlib import Path
import os
import pathlib
import shutil

basedir = "/media/plr/DATA/media/img/HollyVipergirls"

direct_link_source = "/media/plr/DATA/media/gallery-dl/directlink"

http_prefix_len = len("https://")
def main():

    # Opening JSON file
    f = open('json_data.json')

    data = json.load(f)

    for i in data:

        if i['name'] != i['name2']:
            #print(1, i['name'])
            #print(2, i['name2'])
            print("Page: ", i['page'])

            if len(i['name2']) <= 2:
                i['name2'] = i['name']
            
            print(0, i['name2'])


    for i in data:
        new_path = os.path.join(basedir, i['name2'])

        links = i['links']

        img_id = 1
        for url in links:

            #its direct link
            if url.endswith('.jpg'):
                url = url.replace("/", "_")
                url = url[http_prefix_len:]
                #print(url)

                img_path = os.path.join(direct_link_source, url)

                new_file = "image_{:03d}.jpg".format(img_id)
                exist = os.path.exists(img_path)
                print(url, "exist", exist)
                
                if exist:
                    print(new_file)
                    new_path = os.path.join(basedir, i['name2'], new_file)
                    shutil.move(img_path, new_path)

            img_id += 1


    


if __name__ == '__main__':
    #testJson()
    main()


""" 
    for i in data:
        new_path = os.path.join(basedir, i['name2'])

        pathlib.Path(new_path).mkdir(parents=True, exist_ok=True)  

 """