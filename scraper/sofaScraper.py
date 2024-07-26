import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import requests

import time

import os


def scanMatches(shotmapJSONList, graphJSONList, incidentsJSONList):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll the page to load all content of the page
    time.sleep(0.4)

    roundButton = driver.find_elements(By.CLASS_NAME, "Box.bkrWzf.Tab.cbSGUp.secondary")[2]
    driver.execute_script("arguments[0].click();", roundButton)
    time.sleep(0.4)

    roundCountButton = driver.find_elements(By.CLASS_NAME, "Box.Flex.eJCdjm.bnpRyo")[4]
    try:
        roundCount = int(roundCountButton.text.split(" ")[-1])
    except:
        prevRoundButtonTemp = driver.find_elements(By.CLASS_NAME, "Button.iCnTrv")[0]
        driver.execute_script("arguments[0].click();", prevRoundButtonTemp)
        time.sleep(0.4)
        roundCountButton = driver.find_elements(By.CLASS_NAME, "Box.Flex.eJCdjm.bnpRyo")[4]
        roundCount = int(roundCountButton.text.split(" ")[-1])
    
    for i in range(roundCount):
        try:
            matchButtons = driver.find_elements(By.CLASS_NAME, "Box.dtLxRI")
            for i in matchButtons:
                driver.execute_script("arguments[0].click();", i)
                time.sleep(0.4)

                matchInfo = driver.find_elements(By.CLASS_NAME, "BreadcrumbContent.gWYkXa")[1]
                matchIdElementParent = matchInfo.find_elements(By.TAG_NAME, "li")[2]
                matchIdElement = matchIdElementParent.find_elements(By.XPATH, ".//*")[0]
                matchId = matchIdElement.get_attribute(name="href").split(":")[-1]


                shotmapURL = "https://www.sofascore.com/api/v1/event/" + matchId + "/shotmap"
                graphURL = "https://www.sofascore.com/api/v1/event/" + matchId + "/graph"
                incidentsURL = "https://www.sofascore.com/api/v1/event/" + matchId + "/incidents"

                shotmapJSONList.append(BeautifulSoup(requests.get(shotmapURL).text, "html.parser").prettify())
                graphJSONList.append(BeautifulSoup(requests.get(graphURL).text, "html.parser").prettify())
                incidentsJSONList.append(BeautifulSoup(requests.get(incidentsURL).text, "html.parser").prettify())
                time.sleep(0.4)

            prevRoundButton = driver.find_elements(By.CLASS_NAME, "Button.iCnTrv")[0]
            driver.execute_script("arguments[0].click();", prevRoundButton)
            time.sleep(0.4)
        except Exception as error:
            print(error)

def fileOperationsForSeasons(season, shotmaps, graphs, incidents):
    shotmapFileName = season + "shotmap.txt"
    graphFileName = season + "graph.txt"
    incidentsFileName = season + "incidents.txt"

    shotmapFile = open(shotmapFileName, "w")
    graphFile = open(graphFileName, "w")
    incidentsFile = open(incidentsFileName, "w")

    for i in shotmaps:
        shotmapFile.write(i)
    shotmapFile.close()

    for i in graphs:
        graphFile.write(i)
    graphFile.close()

    for i in incidents:
        incidentsFile.write(i)
    incidentsFile.close()

def scrapeForSeason(seasonName, seasonLink):
    try:
        driver.get(seasonLink)
        time.sleep(0.4)
    except:
        pass

    shotmapsJSON = []
    graphsJSON = []
    incidentsJSON = []

    scanMatches(shotmapsJSON, graphsJSON, incidentsJSON)

    print(str(len(shotmapsJSON)) + " shotmaps have been scraped")
    print(str(len(graphsJSON)) + " graphs have been scraped")
    print(str(len(incidentsJSON))+ " incidents have been scraped")

    fileOperationsForSeasons(seasonName, shotmapsJSON, graphsJSON, incidentsJSON)

options = webdriver.ChromeOptions()
options.set_capability(
    "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
)
options.add_experimental_option("detach", True) # to keep chrome webdriver open after program finishes its execution

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(10)

# run here
scrapeForSeason("LigaP22-23", "https://www.sofascore.com/tournament/football/portugal/liga-portugal-betclic/238#id:42655")


