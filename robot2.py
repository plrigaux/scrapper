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
from urllib.parse import urlencode
from urllib.parse import parse_qs
import shutil
import os.path
from pathlib import Path
import time
import configparser
import utilities
import sys
import urlqueue
import collections

config = configparser.ConfigParser()
config.read('config.ini')
outputDirectory = config['DEFAULT']['outputDirectory']

driver = None


def urlSetParams(originalUrl, params) -> str:
    parsed = urlparse.urlparse(originalUrl)
    print(parsed)
    url_parts = list(parsed)
    print(url_parts)
    query = dict(urlparse.parse_qsl(url_parts[4]))
    print(query)
    query.update(params)
    print(query)

    url_parts[4] = urlencode(query)
    print(url_parts)
    url = urlparse.urlunparse(url_parts)

    return url


def main():

    sg = urlqueue.SourceGetter()

    gallery = 'https://www.imagefap.com/pictures/9170441/Beautiful-Models-KARISSA-D-Gloryland?test=my&view=0'
    gallery = 'https://www.imagefap.com/pictures/9172325/Outdoor-Beauties-NIKI-Naked-on-a-Raft?gid=9172325&page=3&view=0'
    gallery = 'https://www.imagefap.com/pictures/9165282/Kimmy-Granger-Horny-Teen'

    # see all pictures
    params = {'page': '0', 'view': '2'}

    print(gallery)

    # exit()

    global driver
    driver = webdriver.Chrome()

    #gallery = config['DEFAULT']['gallery']

    cleanUrl = setUpGallery(gallery, params)
    print(cleanUrl)

    galleryName = utilities.getGalleryNameFromURL(driver.current_url)

    # find first picture
    xpath = '//*[@id="gallery"]/form/table'

    galleryTable = driver.find_element_by_xpath(xpath)

    listId = galleryTable.find_elements_by_xpath(
        '//table/tbody/tr[2]/td/font[2]/i')

    listURL = galleryTable.find_elements_by_xpath('.//table/tbody/tr[1]/td/a')

    img = galleryTable.find_element_by_xpath('.//table/tbody/tr[1]/td/a/img')

    Picture = collections.namedtuple('Picture', 'index href fileName')

    listOfPics = []
    for i, item in enumerate(listId):
        href = listURL[i].get_attribute('href')
        pic = Picture(i, href, item.text)
        listOfPics.append(pic)

    alt = img.get_attribute('alt')
    print(alt)

    nbOfPics = getNumber(alt)

    print("read: {} found: {}".format(nbOfPics, len(listOfPics)))

    driver.quit()


def setUpGallery(gallery, params):

    cleanUrl = utilities.getGalleryNameFromURL(gallery)

    m = re.search(r'/photo/(\d+)/', gallery)

    if m:
        # you are on photo
        driver.get(gallery)
        # go to the gallery
        element = driver.find_element_by_xpath(
            '//*[@id="main"]/center/table[2]/tbody/tr/td/table/tbody/tr/td/center/div[4]/div[3]/table/tbody/tr[1]/td[2]/a')
        element.click()
        gallery = driver.current_url
    else:
        # you are on the gallery
        #cleanUrl = gallery.rsplit('?', 1)[0]
        cleanUrl = urlSetParams(gallery, params)
        driver.get(cleanUrl)

    url = driver.current_url
    print(url)

    return url


def getOriginalFileName():

    title = driver.title
    print(title)
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


def getNumber(alt) -> int:

    #m = re.search(r"(\d+)\s+of\s+(\d+)pics", alt)
    m = re.search(r"(\d+)\s+of\s+(\d+)\s+pics", alt)

    if m:
        return int(m.group(2))

    return -1


if __name__ == "__main__":
    main()
