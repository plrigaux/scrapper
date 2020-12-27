from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException


class MyDriver():

    def __init__(self, browser):

        if (browser.lower == 'firefox'):
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()   

    def click(self, by):

        	(new WebDriverWait(driver, 10)).until(ExpectedConditions.elementToBeClickable(by));
	driver.findElement(by).click();

    img = WebDriverWait(driver, 15, ignored_exceptions=ignored_exceptions)\
            .until(expected_conditions.presence_of_element_located((By.XPATH, imgpath)))
