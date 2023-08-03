from webdriver import MyDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import configData
import tracker

def main():
    global driver
    driver = MyDriver()

    "https://www.imagefap.com/organizer/514191/NIP"
    multi_gal_url = 'https://www.imagefap.com/organizer/437400/Nude-in-public.com?page='

    #grab galery

    # open page
    driver.get(multi_gal_url)

    driver.find_elements_by_xpath
    #xpath = "//table[@class='blk_galleries']////td[@class='blk_galleries']"
    #xpath = "/html/body/center/table[2]/tbody/tr/td/table/tbody/tr/td/div/center/center/table/tbody/tr/td/table/tbody/tr/td[2]/table[2]/tbody/tr[48]/td[1]/font/a"
    xpath = "/html/body/center/table[2]/tbody/tr/td/table/tbody/tr/td/div/center/center/table/tbody/tr/td/table/tbody/tr/td[2]/table[2]/tbody/tr"
    all_gall = driver.find_elements_by_xpath(xpath)

    print("Nb gal: ", len (all_gall))

    i = 1
    for element in all_gall:   
        href = None
        gal_name = None
        nb = None

        try:
            a = element.find_element(by=By.XPATH, value="./td[1]//a")
            href = a.get_attribute('href')
            gal_name = a.text
        except NoSuchElementException:
            pass

        try:
            a = element.find_element(by=By.XPATH, value="./td[2]")            
            nb = a.text        
        except NoSuchElementException:
            pass

        if nb:
            print("Gallery ", i, ": ", gal_name, href, nb)
            save_gallery(gal_name, href, nb)
            i += 1

    driver.quit()

def save_gallery(name :str, href, nb):

    basicGalleryData = configData.GalleryData()

    basicGalleryData.galleryName = name
    basicGalleryData.galleryURL = href

    try:
        nb = int(nb)
        basicGalleryData.nbOfPics = nb
        tracker.save_a_process_gallery(basicGalleryData, status=tracker.NEW)
    except (ValueError, TypeError):
        pass

    


if __name__ == '__main__':
    main()