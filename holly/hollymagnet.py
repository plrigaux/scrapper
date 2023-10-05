import sys
  
# appending the parent directory path
sys.path.append('..')
  
# importing the methods
from webdriver import MyDriver  


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

from picture import Picture
import base64
from PIL import Image
from pathlib import Path
import time
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

    with open('data.csv', 'r', newline='') as file:
        csv_reader = csv.reader(file)
        line_count = 0
        try:
            for row in csv_reader:
                line_count += 1
                link = row[1]
                print(f'Line {line_count} link: {link}')
                if (line_count <= 240):
                    continue
            
                driver.get(link)

                xpath = '//table[@class="lista"]//td[@class="lista"]/a[2]'
                a_tag = driver.find_element_by_xpath(xpath)
                href = a_tag.get_attribute('href')
            
                data = [line_count, row[0], link, href]

                out_data.append(data)

                print(f'find {href} lines.')
                time.sleep(1)
        except:
            print("An exception occurred")
            
        
        print(f'Processed {line_count} lines.')

    print ("bye")
    
    with open('data3.csv', 'w', newline='') as file:
        writer = csv.writer(file)
         
        writer.writerows(out_data)


import time
if __name__ == '__main__':
    main()
    time.sleep(60)
