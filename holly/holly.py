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
import tracker
import argparse
from pprint import pprint
import csv

driver = None
CAPTCHA_PAGE = 'rl_captcha.php'
# see all pictures
params = {'page': '0', 'view': '2'}

#Picture = collections.namedtuple('Picture', 'index href fileName')


main_url = "https://rarbg.to/torrents.php?search=hollyrandall+com+imageset&category=4&page="

def main():

    global driver 
    driver = MyDriver()

    out_data= []
    print ("hello")

    for i in range(0, 23):
        driver.get(main_url + str(i))

        xpath = '//table[@class="lista2t"]/tbody/tr/td[2]/a'
        all_a = driver.find_elements_by_xpath(xpath)

        #print(all_a)

        for element in all_a:        
            href = element.get_attribute('href')
            text = element.text

            data = [text, href]
            out_data.append(data)
    

    print (out_data)


    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
         
        writer.writerows(out_data)

    print ("bye")
    

import time
if __name__ == '__main__':
    main()
    time.sleep(60)
