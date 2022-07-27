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


def exe(links_loc="data/player_links.json", output_loc="data/raw.json"):

    links = json.load(open(links_loc, 'rb'))
    driver = create_driver()

    data_collection = {}
    for i, (name, link) in enumerate(links.items()):
        print(f"{name}: {link}")
        
        driver.get(link)
        update_element = driver.find_element(By.CLASS_NAME, "update")
        smallbody_element = driver.find_element(By.CLASS_NAME, "smallbody")
        elements_combined_text = f'{update_element.text}\n{smallbody_element.text}'

        data_collection[name] = {
            "id": i,
            "link": link,
            "data": elements_combined_text,
        }

    with open(output_loc, "w") as f:
        json.dump(data_collection, f, indent=4)
