import configData
import glob
import yaml
import os

def main():
    root_dir = configData.getOutputDirectory()
    print("Root dir:", root_dir)

    file_list = glob.glob('./*/!data.yaml', root_dir=root_dir)

    print("File list size:", len(file_list))
    #print(*file_list, sep = "\n")

    for filey in file_list:
        file_path = os.path.join(root_dir, filey)
        with open(file_path, 'r') as stream:
            try :
                data_loaded = yaml.safe_load(stream)

                nbOfPics = data_loaded['nbOfPics']
                nbTotalDownloaded = data_loaded['nbTotalDownloaded']
                
                if nbOfPics != nbTotalDownloaded:
                    print(nbTotalDownloaded, "of", nbOfPics, data_loaded['galleryName'])
                    print(data_loaded['galleryURL'])

            except yaml.YAMLError as exc:
                print(exc)    
            
            except KeyError as exc:
                print(exc, "for gallery", filey)   

if __name__ == '__main__':
    main()