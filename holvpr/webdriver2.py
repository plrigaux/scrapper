from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options
from typing import List

driver_location = '/usr/bin/chromedriver'
binary_location = '/usr/bin/google-chrome'

PAGE_LOAD_TIMEOUT = 45

class MyDriver():

    def __init__(self):


        profile = webdriver.FirefoxProfile()
        profile.set_preference("permissions.default.image", 2)

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)

        options = Options()
        options.profile = profile



        self.driver = webdriver.Firefox(options=options)
        
        #self.driver.set_page_load_timeout(10)


        self.ignored_exceptions = (NoSuchElementException,
                                   StaleElementReferenceException)


    def find_element_by_xpath(self, xpath) -> WebElement:
        #return WebDriverWait(self.driver, 200, ignored_exceptions=self.ignored_exceptions)\     
        #    .until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
        return self.driver.find_element(By.XPATH, xpath)

    def find_elements_by_xpath(self, xpath) -> List[WebElement]:
        #return WebDriverWait(self.driver, 200, ignored_exceptions=self.ignored_exceptions)\
        #    .until(expected_conditions.presence_of_all_elements_located((By.XPATH, xpath)))
        return self.driver.find_elements(By.XPATH, xpath)
    
    def basic_find_elements_by_xpath(self, xpath) -> List[WebElement]:
        print("xpath", xpath)
        return self.driver.find_elements(By.XPATH, xpath)

    def current_url(self) -> str:
        return self.driver.current_url

    def quit(self) -> None:
        self.driver.quit()

    def get(self, url) -> None:
        print("Opening page:", url)
    
        timeout = 0
        while True:
            try:
                self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
                self.driver.get(url)

                print("page got")
                break
            except:
                timeout += 1
                print("Page timeout", timeout)
                if timeout > 3:
                   
                    break

        if timeout > 3:
            print("Page try quit")
        else:
            print("Page opened")

    def title(self) -> str:
        return self.driver.title

    def execute_script(self, script, webElement):
        output = self.driver.execute_script(script, webElement)
        return output

    def save_screenshot(self, path) -> bool:
        return self.driver.save_screenshot(path)
    
    def minimize_window(self):
        self.driver.minimize_window() 
