#
# authors: 
#     Joshua Cao (caoj11@uci.edu)
#     Anthony Luu (luuak@uci.edu)
# 2/10/2020
#
# 
# The main annoyance in scraping google images is that google images has a compressed version for each image
# represent with a URL beginning with 'data' instead of 'http'. To get the original source of the images,
# this script manual clicks on each 'small' image, with xpath SMALL_IMG_XPATH, which loads the html for its
# corresponding 'big' image, represented by BIG_IMG_XPATH.
#
# Since web scraping by nature is dependent on the target, this script may break on google images updates.
# Ideally, the script will be fixed by simply fixing the constants at the top of the file, but there are
# no guarantees.
#
# For clarification, IMG_WAIT_THRESHOLD determines how long to wait for the big image to load. When exceeding this
# threshold, the script will instead download the compressed version of this image. Decrease the threshold to
# (very slightly) decrease runtime, or increase the threshold to (very slightly) increase chances of getting full 
# versions of images.
#

import sys
import os
import urllib.request as ulib
import json
import time
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchElementException

BASE_URL = "https://www.google.com/search?q="
URL_FOOTER = "&client=firefox-b-1-d&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj5r9PdotPjAhVmFTQIHfG4C8QQ_AUIEigC&biw=798&bih=1079"

SMALL_IMG_XPATH = "//*[@id=\"islrg\"]/div[1]/div/a[1]/div[1]/img"
BIG_IMG_XPATH = "//*[@id=\"Sva75c\"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img"

IMG_WAIT_THRESHOLD = 3

BASE_SAVE_URL = "images/"

def get_links(search_term):
    start = time.time()
    print("extracting links from google images")
    
    search_term = search_term.replace(' ','+')
    url = BASE_URL + search_term + URL_FOOTER

    driver = webdriver.Firefox()
    driver.get(url)
    
    for i in range(3):
        driver.execute_script("window.scrollBy(0,10000)", "")
        time.sleep(1)

    def get_img_src(driver):
        img_ele = driver.find_element_by_xpath(BIG_IMG_XPATH)
        return img_ele.get_attribute("src")            
    
    links = []
    small_imgs = driver.find_elements_by_xpath(SMALL_IMG_XPATH)
    for small_img in small_imgs:
        small_img.click()
        img_src = get_img_src(driver)
        load_time = time.time()
        while time.time()-load_time < IMG_WAIT_THRESHOLD:
            img_src = get_img_src(driver)
            if img_src[0:4] != "data":
                break
        links.append(img_src)
    driver.close()
            
    print("time elapsed extracting image URLs: ", time.time() - start, " seconds")
    print("number of image URLs: ", len(links))
    return links

def save_images(links, search_term):
    start = time.time()
    print("saving images to local machine")
    
    base = BASE_SAVE_URL
    directory = BASE_SAVE_URL + search_term.replace(' ','_')
    if not os.path.isdir(BASE_SAVE_URL):
        os.mkdir(BASE_SAVE_URL)
    if not os.path.isdir(directory):
        os.mkdir(directory)
    for i, link in enumerate(links):
        try:
            save_path = os.path.join(directory,'{}_{:05}.jpg'.format(search_term,i))
            ulib.urlretrieve(link,save_path)
        except:
            print("error in img#", i)
            pass
    print("time elapsed saving images: ", time.time() - start, " seconds")

if __name__=="__main__":
    overall_start = time.time()
    for search_term in sys.argv[1:]:
        print("working on ", search_term)
        start = time.time()
        links = get_links(search_term)
        save_images(links, search_term)
        print("total time elapsed: ", time.time() - start, " seconds\n")
    print("\noverall time elapsed: ", time.time() - overall_start, " seconds")
    
