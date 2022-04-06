from functions.scraper import Parlour
from functions.parser import *

import pandas as pd
import json
import time
import os
import io
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from io import UnsupportedOperation

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver_path = r'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(driver_path, options = options)

sites = [
    "https://www.google.com/search?rlz=1C1CHBF_enSG861SG861&sxsrf=AOaemvK5e3A2oQQU0sfzRR2062ecehSySQ:1643213918874&q=massage+parlours+in+singapore&npsic=0&rflfq=1&rldoc=1&rllag=1327222,103843803,5287&tbm=lcl&sa=X&ved=2ahUKEwirkrLv6M_1AhULgtgFHd9GAecQtgN6BAgMEHQ",
    "https://www.google.com/search?tbs=lf:1,lf_ui:14&tbm=lcl&sxsrf=APq-WBtmWZBfqa83R3FlO6VG0HRcAHQPnw:1644050443532&q=quality+massage+parlours+singapore&rflfq=1&num=10&sa=X&ved=2ahUKEwibtLeVlej1AhUsumMGHVu0Bv4QjGp6BQgZEKIB",

    ]

select_round = input("What round scraping is this?: ")
mkdir = input("Make directory?: ")

if mkdir == 'y':
    try:
        os.makedirs(f"./round {select_round}/processed data")
        os.makedirs(f"./round {select_round}/processed data/reviews")
        os.makedirs(f"./round {select_round}/raw_data")
    except FileExistsError:
        print("Create it manually")

actions = ActionChains(driver)
for site in sites:
    driver.get(site)
    driver.maximize_window()

    count = 0
    while count <= 50:
        link_class = "a.C8TUKc.rllt__link.a-no-hover-decoration"
        links = driver.find_elements_by_css_selector(link_class)
        for link in links:
            lame_name = link.text[0: link.text.find("\n")]
            current_parlour = Parlour(link, driver)
            try:
                current_parlour.get_parlour_data()

            except TimeoutException:
                print(f"Timeout, {lame_name}")
                actions.send_keys(Keys.ESCAPE).perform()
                time.sleep(2)
                continue

            except StaleElementReferenceException:
                print(f"Stale, {lame_name}")
                actions.send_keys(Keys.ESCAPE).perform()
                time.sleep(2)
                continue

            except ElementNotInteractableException:
                print(f"Not interactable", {lame_name})
                actions.send_keys(Keys.ESCAPE).perform()
                time.sleep(2)
                continue

            name = re.sub("[/|]", "", current_parlour.data["Name"])
            file_name = f"./round {select_round}/raw_data/{name}.json"
            with open(file_name, 'w') as f:
                json.dump(current_parlour.data, f, indent = 4)
                count += 1
            print(f"{lame_name}, {count}")

        try:
            next_page = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "pnnext"))
            )
            next_page.click()
        except (StaleElementReferenceException, ElementNotInteractableException, NoSuchElementException, \
            TimeoutException):
            print("No next page")
            break
        finally:
            time.sleep(2)

input()
driver.close()