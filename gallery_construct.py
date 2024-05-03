from common import DOWNLOADED, NEW
from webdriver import MyDriver
from configData import GalleryData
import configData
import utilities
import re
from selenium.webdriver.common.by import By
from picture import Picture
from selenium.common.exceptions import NoSuchElementException
import os.path

PARAMS = {'page': '0', 'view': '2'}

class InvalidGalleryURL(Exception):
    def __init__(self, original_gallery_url :str, current_gallery_url :str, gallery_data : GalleryData):      

        message = f"Inavalid Gallery URL!\n original: {original_gallery_url}\n actual:{current_gallery_url}"      
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        # Now for your custom code...
        self.original_gallery_url = original_gallery_url
        self.current_gallery_url = current_gallery_url
        self.gallery_data = gallery_data


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


def buildGallery(driver: MyDriver, galleryUrl : str) -> GalleryData:

    print("Gallery Url", galleryUrl)
    print("!!!")
  

    basic_gallery_data = basicGallery(driver, galleryUrl)
    print("Basic", basic_gallery_data)

    local_current_gallery_data = get_local_gallery_data(basic_gallery_data)

    theGallery = None

    currentGalleryOK = False
    if local_current_gallery_data:
        
        if basic_gallery_data.nbOfPics != len(local_current_gallery_data.listOfPics):
            print("CURRENT MISMATCH nbOfPics={} listOfPics.len={}".format(local_current_gallery_data.nbOfPics, len(local_current_gallery_data.listOfPics)))
        else:
            currentGalleryOK = True

    if not currentGalleryOK:
        listOfPics = acquirePictures(driver, basic_gallery_data)
        
        basic_gallery_data.listOfPics = listOfPics

        check_local(basic_gallery_data, local_current_gallery_data)
        theGallery = basic_gallery_data
    else: 
        theGallery = local_current_gallery_data


    theGallery.nbOfPics = len(theGallery.listOfPics)
    configData.dumpData(theGallery)

    return theGallery

def check_local(basic_gallery_data :GalleryData, local_current_gallery_data: GalleryData):
 
    print("Check local Drive") 

    gallery_directory = configData.createAndGetOutputDirectory(
        basic_gallery_data.galleryName)
    for pic in basic_gallery_data.listOfPics:
        fileName = os.path.join(gallery_directory, pic.fileName  )
        fileName = os.path.normpath(fileName)

        if os.path.isfile(fileName):
            pic.status = DOWNLOADED 
            print("File", pic.fileName, "exists") 


def basicGallery(driver: MyDriver, galleryUrl : str) -> GalleryData:
    basicGalleryData = GalleryData(galleryUrl)

    cleanGalleryUrl = setUpGallery(driver, galleryUrl)

    driver.get(cleanGalleryUrl)

    current_gallery_url = driver.current_url()
    print("CURRENT GALLERY URL", current_gallery_url)

    if (current_gallery_url == "https://www.imagefap.com/gallery.php") :
        print("BAD GALLERY URL")
        raise InvalidGalleryURL(galleryUrl, current_gallery_url, basicGalleryData)
    

    print('---------------------------------------------------------')
    basicGalleryData.galleryName = utilities.getGalleryNameFromURL(galleryUrl)

    try:
        xpath = '//*[@id="menubar"]/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/b[1]/font'
        galleryNameTitle = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        xpath = '/html/head/title'
        galleryNameTitle = driver.find_element_by_xpath(xpath)


    galleryName2 = utilities.getGalleryName(galleryNameTitle.text)

    if (galleryName2):
        basicGalleryData.galleryName = utilities.getGalleryName(
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

    xpath = '//div[@id="cnt_cats"]/a'
    cats = []
    for we in driver.find_elements_by_xpath(xpath):
        cats.append(we.text)

    print("Gallery Categories", cats)
    basicGalleryData.categories = cats

    return basicGalleryData

def get_local_gallery_data(galleryData: configData.GalleryData) -> GalleryData:
    gallery_directory = configData.createAndGetOutputDirectory(
        galleryData.galleryName)
    print("Local gallery location: ", gallery_directory)
    currentGalleryData = configData.getCurrentData(gallery_directory)

    if currentGalleryData:
        currentGalleryData.galleryURL = galleryData.galleryURL
        currentGalleryData.galleryName = galleryData.galleryName
        currentGalleryData.nbOfPics = galleryData.nbOfPics

        nbTotalDownloaded = 0
        for picture in currentGalleryData.listOfPics:
            if picture.status.upper() == DOWNLOADED:
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
            configData.dumpData(galleryData)
    else:
        galleryData.nbBatchDownloaded = 0
        galleryData.nbTotalDownloaded = 0
        configData.dumpData(galleryData)



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
        pic = Picture(i + cur_index, item.text, NEW, href)
        listOfPics.append(pic)

    print("listOfPics", len(listOfPics))