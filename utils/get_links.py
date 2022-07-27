from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

import json


def create_driver(link):
    """
    Create chrome driver given web link
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(link)

    return driver


def get_player_links_html(driver):
    
    elements_html = []
    next_page = True
    while next_page:
        elements = driver.find_elements(By.CLASS_NAME, 'sort1')
        elements_filtered = [element for element in elements if element.get_attribute('align') == 'LEFT']
        [elements_html.append(element.get_attribute('innerHTML')) for element in elements_filtered]

        try:
            driver.find_element(By.LINK_TEXT, "Next Page").click()
        except NoSuchElementException:
            next_page = False

    return elements_html


def collect_player_links(position_link):

    driver = create_driver(position_link)
    elements_html = get_player_links_html(driver)
    driver.close()

    # iterate over players
    player_links = {}
    fftoday = "https://fftoday.com"
    for element in elements_html:

        # access player name and link to player data within HTML
        player_name = element.replace("</a>", "").split(">")[-1]
        player_link = fftoday + element.split("\"")[1]

        # collect data in dictionary
        player_links[player_name] = player_link

    return player_links


def exe(output_loc="data/player_links.json"):

    
    link = "https://fftoday.com/stats/playerstats.php?Season=2021&GameWeek=&PosID="
    link_suffix = "&LeagueID=17"
    position_ids = [10, 20, 30, 40, 80]
    position_links = [link + str(position_id) + link_suffix for position_id in position_ids]

    player_links = {}
    for position_link in position_links:
        
        player_links_subset = collect_player_links(position_link)
        for name, player_link in player_links_subset.items():
            player_links[name] = player_link 

    with open(output_loc, "w") as f:
        json.dump(player_links, f, indent=4)
    