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

import re
from urllib.request import proxy_bypass, urlopen
import urllib.parse as urlparse
import os.path
import utilities
import urlqueue
import configData
from picture import Picture
import base64
from PIL import Image
from pathlib import Path
import captcha
import time

driver = None
CAPTCHA_PAGE = 'rl_captcha.php'
# see all pictures
params = {'page': '0', 'view': '2'}

#Picture = collections.namedtuple('Picture', 'index href fileName')


def main():
    sg = urlqueue.SourceGetter()

    gallery = sg.getFirstValid()

    mainGalleryGrabber(gallery)


def mainGalleryGrabber(galleryUrl):
    galleryData = configData.GalleryData()
    try:
        mainGalleryGrabber2(galleryUrl, galleryData)
    finally:

        if 'galleryName' in galleryData:
            dirName = configData.createAndGetOutputDirectory(
                galleryData.getGalleryName())
            configData.dumpData(galleryData, dirName)
            print("Gallery directory: " + dirName)

        print("Gallery url: " + galleryData.getGalleryURL())


def mainGalleryGrabber2(galleryUrl, galleryData):
    print(galleryUrl)

    # exit()
    global driver
    driver = MyDriver()

    #gallery = config['DEFAULT']['gallery']

    cleanUrl = setUpGallery(galleryUrl, params)
    print(cleanUrl)

    current_url = driver.current_url()
    print(type(current_url))
    print(current_url)
    if (CAPTCHA_PAGE in current_url):
        handleCaptcha()

    print('---------------------------------------------------------')
    galleryData['galleryName'] = utilities.getGalleryNameFromURL(current_url)
    xpath = '//*[@id="menubar"]/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/b[1]/font'
    galleryNameTitle = driver.find_element_by_xpath(xpath)

    galleryName2 = utilities.getGalleryName(galleryNameTitle.text)

    if (galleryName2):
        galleryData['galleryName'] = utilities.getGalleryName(galleryNameTitle.text)
    
    galleryData['galleryURL'] = utilities.getCleanURL(driver.current_url())
    print(galleryData['galleryName'])

    # find first picture
    xpath = '//*[@id="gallery"]/form/table'
    galleryTable = driver.find_element_by_xpath(xpath)

    listId = galleryTable.find_elements(by=By.XPATH, value='//table/tbody/tr[2]/td/font[2]/i')

    listURL = galleryTable.find_elements(by=By.XPATH, value='.//table/tbody/tr[1]/td/a')

    # get Nb of pics base on page info
    img = galleryTable.find_element(by=By.XPATH, value='.//table/tbody/tr[1]/td/a/img')
    alt = img.get_attribute('alt')
    galleryData['nbOfPics'] = utilities.getNumber(alt)

    listOfPics = []
    for i, item in enumerate(listId):
        href = listURL[i].get_attribute('href')
        pic = Picture(i, href, item.text, 'new')
        listOfPics.append(pic)

    galleryData['listOfPics'] = listOfPics

    print("read: {} found: {}".format(
        galleryData['nbOfPics'], len(galleryData['listOfPics'])))

    thePictureGraber(galleryData)

    print("Download successs!")

    driver.quit()


def thePictureGraber(galleryData):

    dirName = configData.createAndGetOutputDirectory(
        galleryData['galleryName'])
    print("Output dir: " + dirName)
    currentDalleryData = configData.getCurrentData(dirName)

    if currentDalleryData:
        galleryData['listOfPics'] = currentDalleryData['listOfPics']
    else:
        galleryData['nbBatchDownloaded'] = 0
        galleryData['nbTotalDownloaded'] = 0
        configData.dumpData(galleryData, dirName)

    listOfPics = galleryData['listOfPics']
    galleryDataLenght = len(listOfPics)
    nbBatchDownloaded = 0
    nbTotalDownloaded = 0

    # TODO not download option

    # TODO handle https://www.imagefap.com/rl_captcha.php
    # INFO https://gist.github.com/spirkaa/4c3b8ad8fd34324bd307

    for i, picture in enumerate(listOfPics, start=1):
        print(picture)
        if (picture.status == 'new'):
            print("Downloading {} of {} ...".format(i, galleryDataLenght))

            driver.get(picture.href)

            img = findImgNode(galleryData)
            src = img.get_attribute('src')
            picture.imgSrc = src
            print("image: {}".format(src))

            parsedSrc = urlparse.urlparse(src)
            picture.extention = parsedSrc.path.rsplit('.', 1)[-1]

            picture.fileName = findOriginalFileName(
                picture.fileName, driver.title())

            file_name = os.path.join(dirName, picture.fileName)

            if (downloadImage1(src, file_name) == True):
                #downloadImage2(img, file_name)

                picture.status = 'downloaded'
                nbBatchDownloaded = nbBatchDownloaded + 1
                galleryData['nbBatchDownloaded'] = nbBatchDownloaded
                nbTotalDownloaded = nbTotalDownloaded + 1
            else:
                picture.status = 'failed'

        else:
            print("Pass {} of {}".format(i, galleryDataLenght))
            nbTotalDownloaded = nbTotalDownloaded + 1

        galleryData['nbTotalDownloaded'] = nbTotalDownloaded

    print("Output dir: " + dirName)


def downloadImage1(src, file_name):
    try:
        resource = urlopen(src)

        with open(file_name, "wb") as output:
            output.write(resource.read())
            output.close()
        return True
    except:
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


def setUpGallery(gallery, params):

    cleanUrl = utilities.getGalleryNameFromURL(gallery)

    m = re.search(r'/photo/(\d+)/', gallery)

    if m:
        # you are on photo
        driver.get(gallery)
        # go to the gallery
        element = driver.find_element_by_xpath(
            '//*[@id="main"]/center/table[2]/tbody/tr/td/table/tbody/tr/td/center/div[4]/div[3]/table/tbody/tr[1]/td[2]/a')

        galleryLocation = element.get_attribute('href')

        galleryLocation = setUpGallery(galleryLocation, params)
        print("galleryLocation " + galleryLocation)

        driver.get(galleryLocation)
        gallery = driver.current_url
    else:
        # you are on the gallery
        #cleanUrl = gallery.rsplit('?', 1)[0]
        cleanUrl = utilities.urlSetParams(gallery, params)
        driver.get(cleanUrl)

    url = driver.current_url()
    print(url)

    return url


def findOriginalFileName(galleryFileName, pageTitle) -> str:
    fileName = ""
    if (galleryFileName.endswith("...")):
        fileName = utilities.extractFileName(pageTitle)
    else:
        fileName = galleryFileName

    return fileName


def findImgNode(galleryData, callLevel=0):
    imgpath = '//*[@id="slideshow"]/center/div[1]/span/img'
    #imgpath = '/html/body/center/table[2]/tbody/tr/td[1]/table/tbody/tr/td[1]/div/center/table[2]/tbody/tr/td/table/tbody/tr/td/center/table/tbody/tr/td/div[5]/center/div[1]/span/img'
    ignored_exceptions = (NoSuchElementException,
                          StaleElementReferenceException)
    img = None

    # limit the stack
    if (callLevel > 10):
        return img

    try:
        img = WebDriverWait(driver.driver, 5, ignored_exceptions=ignored_exceptions)\
            .until(expected_conditions.presence_of_element_located((By.XPATH, imgpath)))
    except StaleElementReferenceException:
        # find again
        return findImgNode(galleryData, callLevel + 1)
    except TimeoutException:
        print("Time out capturing img on: " + driver.current_url())
        print(galleryData['galleryURL'])
        currentUrl = driver.current_url()
        if (CAPTCHA_PAGE in currentUrl):
            handleCaptcha()
            img = findImgNode(galleryData, callLevel + 1)

    return img


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

    if (level > 10):
        print("captcha", "FAIL")
        raise "Bye"

    captchaXpath = '/html/body/div/form/div[1]/div[2]/img'

    #get_captcha(driver, ele_captcha, "captcha.jpeg")
    #print (ele_captcha)

    img_base64 = driver.driver.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """, driver.driver.find_element("xpath", captchaXpath))

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
    """
    try:
        input.send_keys(Keys.ENTER)
    except StaleElementReferenceException:
        print("input.send_keys(Keys.ENTER)", StaleElementReferenceException)
"""
    current_url = driver.current_url()
    if (CAPTCHA_PAGE in current_url):
        handleCaptcha(level + 1)


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
