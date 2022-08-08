from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

import json
import time


def create_driver(link=None):
    """
    Create chrome driver, get link if available
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    if link:
        driver.get(link)

    return driver


def collect_data(driver, links):

    data_collection = {}
    for i, (name, link) in enumerate(links.items()):
        
        driver.get(link)
        page_element = driver.find_element(By.CLASS_NAME, "bodycontent")

        data_collection[name] = {
            "id": i,
            "timestamp": time.strftime("%m/%d/%Y, %H:%M:%S"),
            "link": link,
            "data": page_element.text,
        }
    
    return data_collection


def exe(links_loc="data/player_links.json", output_loc="data/raw.json"):

    links = json.load(open(links_loc, 'rb'))
    driver = create_driver()
    data_collection = collect_data(driver, links)

    with open(output_loc, "w") as f:
        json.dump(data_collection, f, indent=4)
