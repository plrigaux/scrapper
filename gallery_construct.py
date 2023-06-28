from pprint import pprint
from webdriver import MyDriver
import configData
import utilities
import re
from selenium.webdriver.common.by import By
from picture import Picture


PARAMS = {'page': '0', 'view': '2'}

def setUpGallery(driver : MyDriver, gallery) -> str:
    print("setUpGallery")
    cleanUrl = utilities.getGalleryNameFromURL(gallery)

    m = re.search(r'/photo/(\d+)/', gallery)

    url = None
    if m:
        # you are on photo
        driver.get(gallery)
        # go to the gallery
        element = driver.find_element_by_xpath(
            '//*[@id="main"]/center/table[2]/tbody/tr/td/table/tbody/tr/td/center/div[4]/div[3]/table/tbody/tr[1]/td[2]/a')

        galleryLocation = element.get_attribute('href')

        url = setUpGallery(driver, galleryLocation)
        
    else:
        # you are on the gallery
        #cleanUrl = gallery.rsplit('?', 1)[0]
        url = utilities.urlSetParams(gallery, PARAMS)
        
    print("galleryLocation:" , url)

    return url


def buildGallery(driver: MyDriver, galleryUrl : str) -> configData.GalleryData:

    print("Gallery Url", galleryUrl)
    print("Stuff")
  

    basicGalleryData = basicGallery(driver, galleryUrl)
    print("Basic", basicGalleryData)

    currentGalleryData = getLocal(basicGalleryData)

    theGallery = None

    currentGalleryOK = False
    if currentGalleryData:
        
        if basicGalleryData.nbOfPics != len(currentGalleryData.listOfPics):
            print("Current Mismatch nbOfPics={} listOfPics.len={}".format(currentGalleryData.nbOfPics, len(currentGalleryData.listOfPics)))
        else:
            currentGalleryOK = True

    if not currentGalleryOK:
        listOfPics = acquirePictures(driver, basicGalleryData)
        basicGalleryData.listOfPics = listOfPics
        theGallery = basicGalleryData
    else: 
        theGallery = currentGalleryData

    return theGallery


def basicGallery(driver: MyDriver, galleryUrl : str) -> configData.GalleryData:
    basicGalleryData = configData.GalleryData()

    cleanGalleryUrl = setUpGallery(driver, galleryUrl)

    driver.get(cleanGalleryUrl)


    print('---------------------------------------------------------')
    basicGalleryData.galleryName = utilities.getGalleryNameFromURL(galleryUrl)
    xpath = '//*[@id="menubar"]/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/b[1]/font'
    galleryNameTitle = driver.find_element_by_xpath(xpath)

    galleryName2 = utilities.getGalleryName(galleryNameTitle.text)

    if (galleryName2):
        basicGalleryData['galleryName'] = utilities.getGalleryName(
        galleryNameTitle.text)

    gallery_url = utilities.getCleanURL(driver.current_url())
    basicGalleryData.galleryURL = gallery_url

    print("Gallery Name", basicGalleryData.galleryName)

    # find first picture
    xpath = '//*[@id="gallery"]/form/table'
    galleryTable = driver.find_element_by_xpath(xpath)


    # get Nb of pics base on page info
    img = galleryTable.find_element(
        by=By.XPATH, value='.//table/tbody/tr[1]/td/a/img')
    alt = img.get_attribute('alt')
    basicGalleryData.nbOfPics = utilities.getNumber(alt)

   
    return basicGalleryData

def getLocal(galleryData: configData.GalleryData):
    dirName = configData.createAndGetOutputDirectory(
        galleryData.galleryName)
    print("Output dir: ", dirName)
    currentGalleryData = configData.getCurrentData(dirName)

    if currentGalleryData:
        currentGalleryData.galleryURL = galleryData.galleryURL
        currentGalleryData.galleryName = galleryData.galleryName
        currentGalleryData.nbOfPics = galleryData.nbOfPics

        nbTotalDownloaded = 0
        for picture in currentGalleryData.listOfPics:
            if picture.status == "downloaded":
                nbTotalDownloaded += 1

        currentGalleryData.nbTotalDownloaded = nbTotalDownloaded

    return currentGalleryData

    if currentGalleryData and len(currentGalleryData.listOfPics) > 0:  
        if len(galleryData.listOfPics) == len(currentGalleryData.listOfPics):
            galleryData.listOfPics = currentGalleryData.listOfPics
        elif len(galleryData.listOfPics) >= len(currentGalleryData.listOfPics):
            for picture in galleryData.listOfPics:
                galleryData.listOfPics[picture.index] = currentGalleryData.listOfPics[picture.index]
            
            galleryData.nbBatchDownloaded = 0
            galleryData.nbTotalDownloaded = 0
        else:
            galleryData.nbBatchDownloaded = 0
            galleryData.nbTotalDownloaded = 0
            configData.dumpData(galleryData, dirName)
    else:
        galleryData.nbBatchDownloaded = 0
        galleryData.nbTotalDownloaded = 0
        configData.dumpData(galleryData, dirName)



def acquirePictures(driver : MyDriver, galleryData: configData.GalleryData) -> list:
    #cleanGalleryUrl = setUpGallery(driver, galleryUrl)
    #driver.get(cleanGalleryUrl)

    #print(cleanGalleryUrl)

    #if (CAPTCHA_PAGE in cleanGalleryUrl):
    #    handleCaptcha()


    print('---------------------------------------------------------')
    print("Check pager")
    xpath = '//*[@id="gallery"]//span/a[@class]'
    pageger = driver.basic_find_elements_by_xpath(xpath)
    print("pager len", len(pageger))
    
    pages = set()
    page_id = 0
    pages.add(0)
    listOfPics = []
    while True:
    #pages[0] = galleryData.galleryURL
        for i, pagelink in enumerate(pageger) :
            href = pagelink.get_attribute('href') 
            #print("a text href", pagelink.text, href)

    
            #pages[int(text)] = href
            v = utilities.getPage(href)
            pages.add(v)

        max_p = max(pages)

        acquirePictures_per_page(driver, page_id, galleryData, listOfPics, True)

        page_id += 1

        if page_id > max_p:
            break

        param = {'page': page_id}
        gallery_url = utilities.urlSetParams(galleryData.galleryURL, param)
        driver.get(gallery_url)
        pageger = driver.basic_find_elements_by_xpath(xpath)

    page_list = sorted(pages)
    print("Pages", page_list)


    return listOfPics

def acquirePictures_per_page(driver : MyDriver, page_id : int, galleryData: configData.GalleryData, listOfPics :list, load_page :bool):

    print('----------------Get gallery pictures Page {} -----------------------------------------'.format(page_id))

    # find first picture
    xpath = '//*[@id="gallery"]/form/table'
    galleryTable = driver.find_element_by_xpath(xpath)

    listId = galleryTable.find_elements(
        by=By.XPATH, value='//table/tbody/tr[2]/td/font[2]/i')

    listURL = galleryTable.find_elements(
        by=By.XPATH, value='.//table/tbody/tr[1]/td/a')

    cur_index = len(listOfPics)
    for i, item in enumerate(listId):
        href = listURL[i].get_attribute('href')
        pic = Picture(i + cur_index, href, item.text, 'new')
        listOfPics.append(pic)

    print("listOfPics", len(listOfPics))