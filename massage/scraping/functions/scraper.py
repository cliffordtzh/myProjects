import selenium
import time
import urllib.request as url
import re
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

# Google Search: massage parlours singapore, all businesses in singapore that fall under here

class Parlour:


    def __init__(self, element, driver):
        self.driver = driver
        self.actions = ActionChains(self.driver)
        self.element = element
        self.data = {}
        self.data["Name"] = None
        self.data["Products"] = None
        self.data["Address"] = None
        self.data["Opening Hours"] = None
        self.data["Rating"] = None
        self.data["Reviews"] = None
        self.data["Phone"] = None
        self.data["Website"] = None

    def scroll_down(self):
        scrollable_div = self.driver.find_element_by_class_name("yf")
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)

    def wait(self, selector, time = 2):
        e = WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return e

    def get_parlour_data(self):
        WebDriverWait(self.driver, 1).until(
            EC.invisibility_of_element((By.CSS_SELECTOR, "iframe.PxHPSd"))
        )
        self.element.click()
        time.sleep(0.3)

        # print("Getting name")
        self.get_name()
        # print("Getting products")
        self.get_products()
        # print("Getting address")
        self.get_address()
        # print("Getting openinghours")
        self.get_openinghours()
        # print("Getting website")
        self.get_website()
        # print("Getting phone")
        self.get_phone()
        # print("Getting rating")
        self.get_rating()
        # print("Getting reviews")
        self.get_reviews()
        print("DONE")

    def get_name(self):
        raw_text = self.element.text
        name = raw_text[0: raw_text.find("\n")]
        self.data["Name"] = re.sub("[/|]", "", name)

    def get_products(self):
        parlour_products = {}
        try:
            self.wait("div.sY9Iuf", time = 1)
        except TimeoutException:
            self.data["Products"] = None
            return

        view_all = self.wait("a.laVYkc", time = 3)

        try:
            self.driver.execute_script("arguments[0].click();", view_all)
        except StaleElementReferenceException:
            count = 0
            try:
                while count < 3:
                    self.driver.execute_script("arguments[0].click();", view_all)
            except StaleElementReferenceException:
                return

        WebDriverWait(self.driver, 2).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe.PxHPSd"))
        )

        row_xpath = "//div[@class='f8twAd']"
        product_rows = len(self.driver.find_elements_by_xpath(row_xpath))
        res = {}
        for i in range(1, product_rows+1):
            product_xpath = f"{row_xpath}[{i}]/div[2]/div[@class='J8zyUd']"
            product_count = len(self.driver.find_elements_by_xpath(product_xpath))
            for j in range(1, product_count+1):
                try:
                    name_xpath = f"{product_xpath}[{j}]/a/div[@class='su7Prc LFlj7c prDW']/div[1]"
                    price_xpath = f"{product_xpath}[{j}]/a/div[@class='su7Prc LFlj7c prDW']/div[2]"
                
                    name = self.driver.find_element_by_xpath(name_xpath).text
                    price = self.driver.find_element_by_xpath(price_xpath).text
                    res[name] = price
                except NoSuchElementException:
                    pass

        self.data["Products"] = res

        self.actions.send_keys(Keys.ESCAPE).perform()
        self.driver.switch_to.default_content()

        WebDriverWait(self.driver, 2).until(
            EC.invisibility_of_element((By.CSS_SELECTOR, "iframe.PxHPSd"))
        )
        
    def get_address(self):
        try:
            address_class = "span.LrzXr"
            address = self.wait(address_class, time = 1)
            self.data["Address"] = address.get_attribute("innerHTML")

        except StaleElementReferenceException:
            count = 0
            try:
                while count < 3:
                    address_class = "span.LrzXr"
                    address = self.wait(address_class, time = 1)

                self.data["Address"] = address.get_attribute("innerHTML")
                count += 1

            except StaleElementReferenceException:
                self.data["Address"] = "Info is not retrievable"

        except NoSuchElementException:
            self.data["Address"] = "Info is not retrievable"

    def get_openinghours(self):
        try:
            hours_class_xpath = "//div[@class='vk_bk h-n']"
            hours_button = self.driver.find_element_by_xpath(hours_class_xpath)
            self.driver.execute_script("arguments[0].click();", hours_button)

            expanded_hours = "div.a-h"
            all_hours = self.wait(expanded_hours).text
            self.data["Opening Hours"] = all_hours

        except NoSuchElementException:
            self.data["Opening Hours"] = "Info is not retrievable"
            
        except StaleElementReferenceException:
            try:
                count = 0
                while count < 3:
                    try:
                        hours_class_xpath = "//div[@class='vk_bk h-n']"
                        hours_button = self.driver.find_element_by_xpath(hours_class_xpath)
                        self.driver.execute_script("arguments[0].click();", hours_button)

                        expanded_hours = "div.a-h"
                        all_hours = self.wait(expanded_hours).text

                    except StaleElementReferenceException:
                        pass
                    count += 1
                self.data["Opening Hours"] = all_hours
            except StaleElementReferenceException:
                self.data["Opening Hours"] = "Info is not retrievable"
        

    def get_rating(self):
        try:
            rating_class = "tp9Rdc"
            rating = self.driver.find_element_by_class_name(rating_class).text
            self.data["Rating"] = rating

        except NoSuchElementException:
            self.data["Rating"] = "Info is not retrievable"

    def get_website(self):
        website_class = "ab_button CL9Uqc"
        try:
            website = self.driver.find_element_by_link_text("Website").get_attribute("href")
            self.data["Website"] = website
        except NoSuchElementException:
            self.data["Website"] = "Info is not retrievable"

        except StaleElementReferenceException:
            count = 0
            while count < 3:
                try:
                    website = self.driver.find_element_by_link_text("Website").get_attribute("href")
                    self.data["Website"] = website
                except StaleElementReferenceException:
                    self.data["Website"] = "Info is not retrievable"


    def get_phone(self):
        try:
            link = self.driver.find_element_by_xpath('//a[@data-dtype="d3ph"]/span')
            self.data["Phone"] = link.get_attribute("innerHTML")

        except NoSuchElementException:
            self.data["Phone"] = "Info is not retrievable"

    def load_reviews(self, times):
        try:
            scrollable_div = self.driver.find_element_by_xpath(f'//div[@class="review-dialog-list"]')
            
            count = 0
            while count <= times:
                time.sleep(0.2)
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                count+=1
                
        except StaleElementReferenceException:
            pass

    def get_reviews(self):
        try:
            res = []

            try:
                more_reviews = self.driver.find_element_by_xpath('//a[@data-async-trigger="reviewDialog"]')
                self.driver.execute_script("arguments[0].click();", more_reviews)
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, '//a[@data-async-trigger="review-dialog-list"]')))
            except WebDriverException:
                self.data["Reviews"] = "Too slow, moved on"

            self.load_reviews(10)

            review_author_class = "TSUbDb"
            review_author_review_class = "A503be"
            review_stars_class = "Fam1ne EBe2gf"
            review_message_class = "review-full-text"

            review_box = "fIQYlf" # for jscontroller attribute
            message = "MZnM8e" # for jscontroller attribute
            button_class = "review-more-link" # for class attribute

            parent_xpath = f"//div[@jscontroller='{review_box}']"
            author_xpath = f"/div[@class='jxjCjc']/div[@style='display:block']/div[@class='{review_author_class}']"
            author_reviews_xpath = f"/div[@class='jxjCjc']/div[@class='FGlxyd']/a[@class='Msppse']/span[@class='{review_author_review_class}']"
            ratings_xpath = f"/div[@class='jxjCjc']/div[@style='vertical-align:top']/div[@class='PuaHbe']/g-review-stars/span[@class='{review_stars_class}']"
            messages_xpath = f"/div[@class='jxjCjc']/div[@style='vertical-align:top']/div[@class='Jtu6Td']/span[@jscontroller='{message}']"

            for button in self.driver.find_elements_by_xpath(f"//a[@class='{button_class}']"):
                self.driver.execute_script('arguments[0].click();', button)

            all_reviews = self.driver.find_elements_by_xpath(f"//div[@jscontroller='{review_box}']")
            for i in range(1, len(all_reviews)+1):

                sub_author_xpath = f"({parent_xpath})[{i}]" + author_xpath
                sub_author_reviews_xpath = f"({parent_xpath})[{i}]" + author_reviews_xpath
                sub_ratings_xpath = f"({parent_xpath})[{i}]" + ratings_xpath
                sub_message_xpath = f"({parent_xpath})[{i}]" + messages_xpath

                try:
                    authors = self.driver.find_element_by_xpath(sub_author_xpath).text
                except NoSuchElementException:
                    authors = "No Author"

                try:    
                    author_reviews = self.driver.find_element_by_xpath(sub_author_reviews_xpath).text
                except NoSuchElementException:
                    author_reviews = "No Past Reviews"
                
                try:
                    rating_label = self.driver.find_element_by_xpath(sub_ratings_xpath)
                    ratings = rating_label.get_attribute("aria-label")
                except NoSuchElementException:
                    ratings = "No Ratings"

                try:
                    message = self.driver.find_element_by_xpath(sub_message_xpath).text
                except NoSuchElementException:
                    message = "No Review"

                entry = '\n'.join([authors, author_reviews, ratings, message, '\n'])
                res.append(entry)
        
            self.data["Reviews"] = res

        except KeyError:
            self.data["Reviews"] = "Info is not retrievable"
            print("no review info")
        
        self.actions.send_keys(Keys.ESCAPE).perform()
