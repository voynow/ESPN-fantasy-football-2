from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import time


def create_driver(link):
    """
    Create chrome driver given web link
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(link)

    return driver


def exe():

    link = "https://fftoday.com/stats/playerstats.php?Season=2021&GameWeek=&PosID="
    position_ids = [10, 20, 30, 40]
    links = [link + str(position_id) for position_id in position_ids]

    for link in links:
        driver = create_driver(link)
        time.sleep(2)

        driver.close()
    