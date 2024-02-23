from webdriver import MyDriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


import gallery_construct as gc
from configData import GalleryData

from urllib.request import proxy_bypass, urlopen
import urllib.parse as urlparse
import os.path
import utilities
import urlqueue
import configData

import base64
#from PIL import Image
from pathlib import Path
#import captcha
import time
import tracker
import argparse
from pprint import pprint

driver = None
CAPTCHA_PAGE = 'human-verification'
FAILED = 'failed'
NEW = 'new'
# see all pictures

#Picture = collections.namedtuple('Picture', 'index href fileName')


def main():

    parser = argparse.ArgumentParser(description="Robot scraper",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--notrack", action="store_true",
                        help="don't read tack file")

    args = parser.parse_args()
    cli_config = vars(args)
    print(cli_config)

    source_getter = urlqueue.SourceGetter()

    use_tracker = True
    if cli_config['notrack']:
        print("Don't use tracker")
        use_tracker = False

    while True:
        galleryURL = source_getter.getFirstValid(use_tracker=use_tracker)

        mainGalleryGrabber(galleryURL)
        use_tracker = True


def mainGalleryGrabber(galleryUrl: str):

    galleryData = None
    dirName = "Not defined"

    global driver
    driver = MyDriver()

    try:
        galleryData = gc.buildGallery(driver, galleryUrl)
        tracker.in_progress(galleryData, galleryUrl)
        mainGalleryGrabber2(galleryData)
    finally:
        if galleryData:
            if galleryData.has_key('galleryName'):
                dirName = configData.createAndGetOutputDirectory(
                    galleryData.galleryName)
                configData.dumpData(galleryData, dirName)

            status = "SUCCESS"
            if galleryData.nbOfPics != galleryData.nbTotalDownloaded:
                tracker.failed(galleryData)
                status = tracker.FAILED

        print()
        print()
        print("--------- END ----------")
        print("Gallery directory: ", dirName)
        print("Gallery url: ", galleryData.galleryURL)
        print("Gallery name: ", galleryData.galleryName)
        print("Gallery number of files: ", galleryData.nbOfPics)
        print("Gallery file dowloaded: ", galleryData.nbTotalDownloaded)
        print(status)
        print()
        print()


def mainGalleryGrabber2(galleryData: configData.GalleryData):
    print(galleryData.galleryURL)
    print("Stuff")
    pprint(galleryData)

    print("Load the list")
    #LOAD_AGAIN = True
    LOAD_AGAIN = False

    if len(galleryData.listOfPics) > 0 and not LOAD_AGAIN:
        print("Don't get pictures list")
        pass
    else:
        listOfPics = gc.acquirePictures(driver, galleryData)

        configData.updateList(galleryData, listOfPics)

        tracker.save_a_process_gallery(galleryData)

        print("read: {} found: {}".format(
            galleryData.nbOfPics, len(galleryData.listOfPics)))

        pprint(galleryData.listOfPics, depth=3)

    thePictureGraber(galleryData)

    print("Download successs!")
    tracker.success(galleryData)

    driver.quit()


def thePictureGraber(galleryData):
    dirName = configData.createAndGetOutputDirectory(
        galleryData.galleryName)
    print("Output dir: ", dirName)
    listOfPics = galleryData.listOfPics
    galleryDataLenght = len(listOfPics)
    nbBatchDownloaded = 0
    nbTotalDownloaded = 0

    print("Going to dowload a gallery of '{}' items".format(galleryDataLenght))
    # TODO not download option

    # TODO handle https://www.imagefap.com/rl_captcha.php
    # INFO https://gist.github.com/spirkaa/4c3b8ad8fd34324bd307
    driver.minimize_window()
    
    for i, picture in enumerate(listOfPics, start=1):
        print(picture)
        if (picture.status == NEW):
            print("Downloading {} of {} ...".format(i, galleryDataLenght))

            # open page
            driver.get(picture.href)

            if driver.current_url == "https://www.imagefap.com/human-verification":
                break

            img = findImgNode(galleryData)
            if img is not None:
                src = img.get_attribute('src')
                picture.imgSrc = src
                print("image: {}".format(src))

                parsedSrc = urlparse.urlparse(src)
                picture.extention = parsedSrc.path.rsplit('.', 1)[-1]

                picture.fileName = findOriginalFileName(
                    picture.fileName, driver.title())

                file_name = get_file_name(dirName, picture)

                nbTotalDownloaded = downloadImage(galleryData, nbBatchDownloaded, nbTotalDownloaded, picture, file_name)
        elif (picture.status == FAILED):
            file_name = get_file_name(dirName, picture)
            nbTotalDownloaded = downloadImage(galleryData, nbBatchDownloaded, nbTotalDownloaded, picture, file_name)
        else:
            print("Pass {} of {}".format(i, galleryDataLenght))
            nbTotalDownloaded = nbTotalDownloaded + 1

        galleryData['nbTotalDownloaded'] = nbTotalDownloaded

    print("Output dir: " + dirName)

def get_file_name(dirName, picture):
    fn = picture.fileName
    fn = fn.rsplit('/', 1)[-1]
    file_name = os.path.join(dirName, fn)
    return file_name

def downloadImage(galleryData : GalleryData, nbBatchDownloaded: int, nbTotalDownloaded : int, picture, file_name) -> int:
    if (downloadImage1(picture.imgSrc, file_name) == True):
                #downloadImage2(img, file_name)
        picture.status = 'downloaded'
        nbBatchDownloaded = nbBatchDownloaded + 1
        galleryData['nbBatchDownloaded'] = nbBatchDownloaded
        nbTotalDownloaded = nbTotalDownloaded + 1
    else:
        if picture.status == FAILED:
            picture.status = NEW
        else:
            picture.status = FAILED
    return nbTotalDownloaded


def downloadImage1(src, file_name):
    try:
        print("download image")
        resource = urlopen(src, timeout=10)

        if resource is None:
            print("No image", src)
            return False

        with open(file_name, "wb") as output:
            output.write(resource.read())
            output.close()
        return True
    except Exception as exp:
        print("Exeption image", src, exp)
        return False


def downloadImage2(img, file_name):
    #get_captcha(driver, ele_captcha, "captcha.jpeg")
    #print (ele_captcha)

    # img_base64 = driver.driver.execute_script("""
    # var ele = arguments[0];
    # var cnv = document.createElement('canvas');
    #cnv.width = ele.width; cnv.height = ele.height;
    #cnv.getContext('2d').drawImage(ele, 0, 0);
    # return cnv.toDataURL('image/jpeg').substring(22);
    # """, img)

    img_base64 = driver.driver.execute_async_script("""
    var ele = arguments[0], callback = arguments[1];
    ele.addEventListener('load', function fn(){
      ele.removeEventListener('load', fn, false);
      var cnv = document.createElement('canvas');
      cnv.width = this.width; cnv.height = this.height;
      cnv.getContext('2d').drawImage(this, 0, 0);
      callback(cnv.toDataURL('image/jpeg').substring(22));
    }, false);
    ele.dispatchEvent(new Event('load'));
    """, img)

    with open(file_name, 'wb') as f:
        f.write(base64.b64decode(img_base64))


def findOriginalFileName(galleryFileName, pageTitle) -> str:
    fileName = ""
    if (galleryFileName.endswith("...")):
        fileName = utilities.extractFileName(pageTitle)
    else:
        fileName = galleryFileName

    return fileName


def findImgNode(galleryData, callLevel=0) -> WebElement | None:
    imgpath = '//*[@id="slideshow"]/center/div[1]/span/img'
    #imgpath = '/html/body/center/table[2]/tbody/tr/td[1]/table/tbody/tr/td[1]/div/center/table[2]/tbody/tr/td/table/tbody/tr/td/center/table/tbody/tr/td/div[5]/center/div[1]/span/img'
    ignored_exceptions = (NoSuchElementException,
                          StaleElementReferenceException)
    img = None

    # limit the stack
    if (callLevel > 20):
        return img

    try:
        img: WebElement = WebDriverWait(driver.driver, 15, ignored_exceptions=ignored_exceptions)\
            .until(expected_conditions.presence_of_element_located((By.XPATH, imgpath)))
    except StaleElementReferenceException:
        # find again
        print("Find again img")
        return findImgNode(galleryData, callLevel + 1)
    except TimeoutException:
        print("Time out capturing img on: " + driver.current_url())
        print(galleryData['galleryURL'])
        currentUrl = driver.current_url()
        if (CAPTCHA_PAGE in currentUrl):
            handleCaptcha()
            if callLevel > 2:
                exit()
            img = findImgNode(galleryData, callLevel + 1)

    return img


"""
def contextMenuClick(element : WebElement):
    evt = element.ownerDocument.createEvent('MouseEvents')

    RIGHT_CLICK_BUTTON_CODE = 2; # the same for FF and IE

    evt.initMouseEvent('contextmenu', True, True,
         element.ownerDocument.defaultView, 1, 0, 0, 0, 0, false,
         false, false, false, RIGHT_CLICK_BUTTON_CODE, None)

    if element.ownerDocument.createEventObject:
        # dispatch for IE
       return element.fireEvent('onclick', evt)
    
    else:
    # dispatch for firefox + others
      return !element.dispatchEvent(evt)
    
"""


def removePopup():
    xpbtn = '/html/body/div[3]/div/div[1]/div'
    try:
        popup = driver.find_element("xpath", xpbtn)
        print("remove the add pop-up")
        popup.click()
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass

def handleCaptcha(level=0):
    print("Captcha detected")
    pass

"""
def handleCaptcha(level=0):

    if (level > 10):
        print("captcha", "FAIL")
        raise "Bye"

    captchaXpath = '/html/body/div/form/div[1]/div[2]/img'

    #get_captcha(driver, ele_captcha, "captcha.jpeg")
    #print (ele_captcha)

    #img_base64 = driver.driver.execute_script(
    #var ele = arguments[0];
    #var cnv = document.createElement('canvas');
    #cnv.width = ele.width; cnv.height = ele.height;
    #cnv.getContext('2d').drawImage(ele, 0, 0);
    #return cnv.toDataURL('image/jpeg').substring(22);    
    #, driver.driver.find_element("xpath", captchaXpath))

    dirPath = "stuff"
    Path(dirPath).mkdir(parents=True, exist_ok=True)

    captchaPath = os.path.join(dirPath, "captcha.jpg")
    with open(captchaPath, 'wb') as f:
        f.write(base64.b64decode(img_base64))

    code = captcha.solve_captcha(captchaPath)
    print("THE CAPTCHA IS: ", code)

    inputXpath = '//*[@id="captcha"]'

    input = driver.find_element("xpath", inputXpath)

    input.send_keys(code)
    time.sleep(2)

    #try:
    #    input.send_keys(Keys.ENTER)
    #except StaleElementReferenceException:
    #    print("input.send_keys(Keys.ENTER)", StaleElementReferenceException)

    current_url = driver.current_url()
    if (CAPTCHA_PAGE in current_url):
        handleCaptcha(level + 1)

"""

def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)

    left = location['x']
    top = location['y'] + 140
    right = location['x'] + size['width']
    bottom = location['y'] + size['height'] + 140

    image = image.crop((left, top, right, bottom))  # defines crop points
    image = image.convert('RGB')
    image.save(path, 'jpeg')  # saves new cropped image


if __name__ == '__main__':
    main()
