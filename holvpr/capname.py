from dataclasses import dataclass
import sys
import pprint
import json
# importing the methods
from webdriver2 import MyDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


link = "https://vipergirls.to/threads/6907891-Holly-Randall"


class Gallery:

    def __init__(self, name, name2, pagenb, links):
        self.name = name
        self.name2 = name2
        self.page = pagenb
        self.nbinks = len(links)
        self.links = links

def to_json(obj):
    return json.dumps(obj, default=lambda obj: obj.__dict__)

""" def testJson():
    gal_links_href_list = ["sdf", "asdfas", "4564536"]
    gal = Gallery("h2_text", "blockquote_text", gal_links_href_list)
    gal2 = Gallery("h2_text2", "blockquote_text", gal_links_href_list)
    
    l = [gal, gal2]
    y = to_json(l)
    print(y)
    y = json.dumps(to_json(gal))
    print(y)
    
    json.dump({"foo": json.dumps([{"bar": 1}, {"baz": 2}])},sys.stdout) """
    


def main():
    driver = MyDriver()
    gal_list = []


    for x in range(1, 34):

        page = link
        if x > 1:
            page = link + "/page" + str(x)
        
        scrap_link(driver, gal_list, page, x)

    json_data = to_json(gal_list)
    #print(y)
    with open("json_data.json", "w") as outfile:
        outfile.write(json_data)


def scrap_link(driver:MyDriver, gal_list:list, page:str, pagenb:int):
    driver.get(page)

    xpath = '//div[@class="postdetails"]/div[@class="postbody"]'
    list = driver.find_elements_by_xpath(xpath)

  
    for a in list:

        h2_text = ""
        blockquote_text = ""
        # print("TITLE", a.text)
        try:
            h = a.find_element(By.XPATH, './/h2')
            # print("H2", h.tag_name, h.text)
            h2_text = h.text
        except NoSuchElementException:
            print("not found h2")

        gal_links = []
        try:
            bk = a.find_element(By.XPATH, './/blockquote')
            # print("blockquote", bk.tag_name, bk.text)
            blockquote_text = bk.text

            gal_links = bk.find_elements(By.XPATH, './/a[img]')
        except NoSuchElementException:
            print("not found blockquote")

        print("-----------------------")
        print(h2_text)
        

        idx = blockquote_text.find('\n')
        if idx >= 0:
            blockquote_text = blockquote_text[0:idx]
            # print("sub", idx, blockquote_text)

        print(blockquote_text)

        gal_links_href_list = []

        for img_ref in gal_links:
            gal_links_href = img_ref.get_property("href")
            # print("a", gal_links_href)
            gal_links_href_list.append(gal_links_href)

        gal = Gallery(h2_text, blockquote_text, pagenb, gal_links_href_list)
        gal_list.append(gal)

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(gal_list)




if __name__ == '__main__':
    #testJson()
    main()
