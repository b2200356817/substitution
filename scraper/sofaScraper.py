import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import requests

import time

def scanMatches(shotmapJSONList, graphJSONList, incidentsJSONList):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll the page to load all content of the page
    time.sleep(0.4)

    roundButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div[3]/div/div[1]/div[1]/div[5]/div/div[2]/div[2]")
    driver.execute_script("arguments[0].click();", roundButton)
    time.sleep(0.4)

    matchesPerRound = 1
    try:
        while(True):
            matchButton = driver.find_element(By.XPATH, ("//html/body/div[1]/main/div/div[3]/div/div[1]/div[1]/div[5]/div/div[3]/div/div/div[1]/div/div[2]/a[" + str(matchesPerRound) + "]/div/div/div[4]"))
            driver.execute_script("arguments[0].click();", matchButton)
            matchesPerRound += 1
            time.sleep(0.4)

            matchId = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div[3]/div/div[1]/div[1]/div[5]/div/div[3]/div/div/div[2]/div/div[1]/div/div[1]/div[1]/ul/li[3]/a")
            shotmapURL = "https://www.sofascore.com/api/v1/event/" + matchId.get_attribute(name="href").split(":")[-1] + "/shotmap"
            graphURL = "https://www.sofascore.com/api/v1/event/" + matchId.get_attribute(name="href").split(":")[-1] + "/graph"
            incidentsURL = "https://www.sofascore.com/api/v1/event/" + matchId.get_attribute(name="href").split(":")[-1] + "/incidents"

            shotmapJSONList.append(BeautifulSoup(requests.get(shotmapURL).text, "html.parser").prettify())
            graphJSONList.append(BeautifulSoup(requests.get(graphURL).text, "html.parser").prettify())
            incidentsJSONList.append(BeautifulSoup(requests.get(incidentsURL).text, "html.parser").prettify())
            time.sleep(0.4)
    except:
        pass



options = webdriver.ChromeOptions()
options.set_capability(
    "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
)
options.add_experimental_option("detach", True) # to keep chrome webdriver open after program finishes its execution

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(10)

try:
    driver.get("https://www.sofascore.com/tournament/football/england/premier-league/17#id:41886")
except:
    pass

shotmapsJSON = []
graphsJSON = []
incidentsJSON = []

scanMatches(shotmapsJSON, graphsJSON, incidentsJSON)
