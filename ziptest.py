from zipfile import ZipFile
  
# specifying the zip file name
file_name = "/tmp/zipstream/tokio/test_lzma1.zip"
  
# opening the zip file in READ mode
with ZipFile(file_name, 'r') as zip:
    # printing all the contents of the zip file
    zip.printdir()
    info = zip.getinfo("file1.txt")
    print(info)
  
    # extracting all the files
    print('Extracting all the files now...')
    #zip.extractall()
    print('Done!')