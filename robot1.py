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
from urllib.request import urlretrieve
from urllib.request import urlopen
import urllib.parse as urlparse
from urllib.parse import parse_qs
import shutil
import os.path
from pathlib import Path
import time
import configparser
import utilities
import sys
import urlqueue

config = configparser.ConfigParser()
config.read('config.ini')
outputDirectory = config['DEFAULT']['outputDirectory']


def main():

    sg = urlqueue.SourceGetter()
    
    gallery = sg.getFirstValid()

    global driver
    driver = webdriver.Chrome()

    #gallery = 'https://www.imagefap.com/pictures/9147089/Nevaeh-Sniper'
    #gallery = 'https://www.imagefap.com/pictures/9157754/The-Simpson%27s-Merry-Christmas'
    #gallery = 'https://www.imagefap.com/pictures/9160455/Theresa-Presenting-Theresa?gid=9160455&page=5&view=0'
    #gallery = 'https://www.imagefap.com/pictures/9160216/Valory-Irene-Katerina-Hartlova-%7C-Good-Morning?gid=9160216&page=2&view=0'
    #gallery = 'https://www.imagefap.com/pictures/8320839/Brittany-Bardot-gets-Rachels-fist-up-her-bum'
    #gallery = "https://www.imagefap.com/photo/683150892/?pgid=&gid=8021417&page=0&idx=18"
    #gallery = 'https://www.imagefap.com/photo/872088544/?pgid=&gid=8068100&page=0&idx=2'
    #gallery = 'https://www.imagefap.com/pictures/9166638/Swiss-Conceptual-Performance-Artist-Milo-Moire.-Extasia'
    #gallery = 'https://www.imagefap.com/pictures/9171882/Nathalie-la-petite-hotesse.-French-comic-%2F-BD'
    #gallery = 'https://www.imagefap.com/pictures/9173133/Sensual-Jane-Big-Time-Sensuality?gid=9173133&page=3&view=0'
    #gallery = 'https://www.imagefap.com/pictures/9167640/Peta-Jensen-Horny-Slut'

    #gallery = config['DEFAULT']['gallery']



    cleanUrl = setUpGallery(gallery)
    print(cleanUrl)
    

    galleryName = utilities.getGalleryNameFromURL(driver.current_url)

    # find first picture
    xpath = '/html/body/center/table[2]/tbody/tr/td[1]/table/tbody/tr/td[1]/div/center/table/tbody/tr/td/table/tbody/tr/td/center/div[1]/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/a'
    firstLink = driver.find_element_by_xpath(xpath)
    firstLink.click()

    i = 1
    imgIndex = -1
    lastsrc = ""
    while True:
        newImgIndex = getImgIndex(driver.current_url)

        if (newImgIndex < imgIndex):
            print("End loop! {} iteration done".format(i - 1))
            break

        imgIndex = newImgIndex

        src = findImgUrl()

        while src == lastsrc:
            print("go get new src")
            removePopup()
            time.sleep(1)
            src = findImgUrl()

        lastsrc = src

        print("src ------------------------")
        print(src)
        originalFileName = getOriginalFileName()
        print(originalFileName)

        dirName = os.path.join(outputDirectory, galleryName)
        Path(dirName).mkdir(parents=True, exist_ok=True)

        parsedSrc = urlparse.urlparse(src)
        extention = parsedSrc.path.rsplit('.', 1)[-1]

        file_name = os.path.join(dirName, "img_{:03d}.{}".format(i, extention))

        resource = urlopen(src)
        output = open(file_name, "wb")
        output.write(resource.read())
        output.close()

        i = i + 1
        # next picture
        nextPicture()
    
    driver.quit()

def setUpGallery(gallery):

    cleanUrl = utilities.getGalleryNameFromURL(gallery)

    m = re.search(r'/photo/(\d+)/', gallery)

    if m:
        #you are on photo
        driver.get(gallery) 
        #go to the gallery
        element = driver.find_element_by_xpath('//*[@id="main"]/center/table[2]/tbody/tr/td/table/tbody/tr/td/center/div[4]/div[3]/table/tbody/tr[1]/td[2]/a')
        element.click()
        gallery = driver.current_url
    else: 
        #you are on the gallery
        cleanUrl = gallery.rsplit('?', 1)[0]
        driver.get(cleanUrl)

    url = driver.current_url
    print(url)

    return url

def getOriginalFileName():
    
    title = driver.title
    print (title)
    match = re.search(r'.*?\.\w+', title)

    return match.group(0)

def getImgIndex(current_url):
    print(current_url)
    parsed = urlparse.urlparse(current_url)

    print(parsed.fragment)

    fragment = -1

    try:
        fragment = int(parsed.fragment)
    except ValueError:
        pass

    return fragment


def findImgUrl():
    imgpath = '//*[@id="slideshow"]/center/div[1]/span/img'
    #imgpath = '/html/body/center/table[2]/tbody/tr/td[1]/table/tbody/tr/td[1]/div/center/table[2]/tbody/tr/td/table/tbody/tr/td/center/table/tbody/tr/td/div[5]/center/div[1]/span/img'
    ignored_exceptions = (NoSuchElementException,
                          StaleElementReferenceException)
    try:
        img = WebDriverWait(driver, 15, ignored_exceptions=ignored_exceptions)\
            .until(expected_conditions.presence_of_element_located((By.XPATH, imgpath)))

        src = img.get_attribute('src')
    except StaleElementReferenceException:
        # find again
        return findImgUrl()

    return src


def nextPicture():
    #xpathNextbutton = '//*[@id="controls"]/div/a[2]'
    xpathNextbutton = '/html/body/center/table[2]/tbody/tr/td[1]/table/tbody/tr/td[1]/div/center/table[2]/tbody/tr/td/table/tbody/tr/td/center/table/tbody/tr/td/div[2]/div/a[2]'
    nextbutton = driver.find_element_by_xpath(xpathNextbutton)
    try:
        nextbutton.click()
    except ElementClickInterceptedException:
        removePopup()
        nextPicture()


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


main()
