import os
from requests import get
from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import urllib.request


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

for image in os.listdir("src"):
    if not os.path.isfile("preview/"+image):
        driver.get('https://deadbydaylight.fandom.com/wiki/'+image.replace(".png", ""))
        img = driver.find_element(By.CLASS_NAME, "infoboxtable")
        print(img)
        img = img.find_element(By.XPATH, '//tbody/tr[2]/td/a/img')
        print(img)
        urllib.request.urlretrieve(img.get_attribute("src"), "preview/"+image)
        print(image, "success")