from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.remote.webelement import WebElement


class MyDriver():

    def __init__(self):
        self.driver = webdriver.Chrome()

        #fFprofile = webdriver.FirefoxProfile()
        # I also tried True, 1 - with and without quotes
        #fFprofile.set_preference(   'network.websocket.allowInsecureFromHTTPS', True)
        #fFprofile.DEFAULT_PREFERENCES['frozen']["dom.disable_open_during_load"] = True
# FFprofile = webdriver.FirefoxProfile('C:/Users/ExampleUser/AppData/Local/Mozilla/Firefox/Profiles/owieroiuysd.testprofile')

        #self.driver = webdriver.Firefox(firefox_profile = fFprofile)
        #self.driver = webdriver.Firefox()
        self.ignored_exceptions = (NoSuchElementException,
                                   StaleElementReferenceException)

    def find_element_by_xpath(self, xpath) -> WebElement:
        return WebDriverWait(self.driver, 200, ignored_exceptions=self.ignored_exceptions)\
            .until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))

    def current_url(self) -> str:
        return self.driver.current_url

    def quit(self) -> None:
        self.driver.quit()

    def get(self, url) -> None:
        self.driver.get(url)

    def title(self) -> str:
        return self.driver.title

    def execute_script(self, script, webElement):
        output = self.driver.execute_script(script, webElement)
        return output

    def save_screenshot(self, path) -> bool:
        return self.driver.save_screenshot(path)
