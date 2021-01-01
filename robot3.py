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

import re
from urllib.request import urlopen
import urllib.parse as urlparse
import os.path
import utilities
import urlqueue
import configData
from picture import Picture

driver = None

# see all pictures
params = {'page': '0', 'view': '2'}

#Picture = collections.namedtuple('Picture', 'index href fileName')


def main(galleryData):

    sg = urlqueue.SourceGetter()

    gallery = sg.getFirstValid()

    print(gallery)

    # exit()
    global driver
    driver = MyDriver()

    #gallery = config['DEFAULT']['gallery']

    cleanUrl = setUpGallery(gallery, params)
    print(cleanUrl)

    current_url = driver.current_url()
    print(type(current_url))
    print(current_url)
    print('---------------------------------------------------------')
    galleryData['galleryName'] = utilities.getGalleryNameFromURL(current_url)
    galleryData['galleryURL'] = current_url
    xpath = '//*[@id="menubar"]/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/b[1]/font'
    galleryNameTitle = driver.find_element_by_xpath(xpath)
    galleryData['galleryName'] = utilities.getGalleryName(
        galleryNameTitle.text)
    galleryData['galleryURL'] = driver.current_url()
    print(galleryData['galleryName'])

    # find first picture
    xpath = '//*[@id="gallery"]/form/table'

    galleryTable = driver.find_element_by_xpath(xpath)

    listId = galleryTable.find_elements_by_xpath(
        '//table/tbody/tr[2]/td/font[2]/i')

    listURL = galleryTable.find_elements_by_xpath('.//table/tbody/tr[1]/td/a')

    # get Nb of pics base on page info
    img = galleryTable.find_element_by_xpath('.//table/tbody/tr[1]/td/a/img')
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

    #TODO not download option

    #TODO handle https://www.imagefap.com/rl_captcha.php

    for i, picture in enumerate(listOfPics, start = 1):
        print(picture)
        if (picture.status == 'new'):
            print("Downloading {} of {} ...".format(i, galleryDataLenght))

            driver.get(picture.href)

            src = findImgUrl()
            print("image: {}".format(src))

            parsedSrc = urlparse.urlparse(src)
            picture.extention = parsedSrc.path.rsplit('.', 1)[-1]

            picture.fileName = findOriginalFileName(
                picture.fileName, driver.title())

            file_name = os.path.join(dirName, picture.fileName)

            resource = urlopen(src)
            output = open(file_name, "wb")
            output.write(resource.read())
            output.close()

            picture.status = 'downloaded'
            nbBatchDownloaded = nbBatchDownloaded + 1
            galleryData['nbBatchDownloaded'] = nbBatchDownloaded
            galleryData['nbTotalDownloaded'] = i
        else:
            print("Pass {} of {}".format(i, galleryDataLenght))

    print("Output dir: " + dirName)


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


def findImgUrl():
    imgpath = '//*[@id="slideshow"]/center/div[1]/span/img'
    #imgpath = '/html/body/center/table[2]/tbody/tr/td[1]/table/tbody/tr/td[1]/div/center/table[2]/tbody/tr/td/table/tbody/tr/td/center/table/tbody/tr/td/div[5]/center/div[1]/span/img'
    ignored_exceptions = (NoSuchElementException,
                          StaleElementReferenceException)
    try:
        img = WebDriverWait(driver.driver, 15, ignored_exceptions=ignored_exceptions)\
            .until(expected_conditions.presence_of_element_located((By.XPATH, imgpath)))

        src = img.get_attribute('src')
    except StaleElementReferenceException:
        # find again
        return findImgUrl()

    return src


def removePopup():
    xpbtn = '/html/body/div[3]/div/div[1]/div'
    try:
        popup = driver.find_element_by_xpath(xpbtn)
        print("remove the add pop-up")
        popup.click()
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass


galleryData = {}
try:
    main(galleryData)
finally:

    if 'galleryName' in galleryData:
        dirName = configData.createAndGetOutputDirectory(
            galleryData['galleryName'])
        configData.dumpData(galleryData, dirName)
        print("Gallery directory: " + dirName)
