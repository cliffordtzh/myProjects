import urllib.request as url
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


def scrape(site_link):
    # Requesting access to website
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             'Chrome/78.0.3904.108 Safari/537.36'}
    request = url.Request(site_link, None, headers)
    response = url.urlopen(request)
    source = response.read().decode('utf-8')

    # regex patterns for emails and phone numbers
    e_pattern = '[a-zA-z0-9]+@[a-zA-z]+\\.[(com|sg)]+[\\.sg]*'
    p_pattern = '\\(?\\+?\\(?65\\)?\\)?\\s?\\(?[6|9|8][0-9]{3}\\s?[0-9]{4}\\)?'

    # Contact details found are kept in a list
    emails_list = []
    [emails_list.append(mail) for mail in re.findall(e_pattern, source) if mail not in emails_list]
    numbers_list = []
    [numbers_list.append(no) for no in re.findall(p_pattern, source) if no not in numbers_list]

    # Returns either the first contact found, or none
    if len(emails_list) == 0:
        emails_list = ['No Email']
    elif len(emails_list) > 1:
        emails_list = emails_list[0]

    if len(numbers_list) == 0:
        numbers_list = ['No Numbers']
    elif len(numbers_list) > 1:
        numbers_list = numbers_list[0:1]

    # Reformatting the number
    formatted_numbers_list = []
    for number in numbers_list:
        if len(number) > 8 and number != 'No Numbers':
            unwanted = ['(', ')', '+', ' ']
            for symbol in unwanted:
                if symbol in number:
                    number = number.replace(symbol, '')
            if number[0:2] == '65':
                number = number[2:]
            formatted_numbers_list.append(number)

    return emails_list, formatted_numbers_list


"""
Scraping from a webpage listing other websites. E.g. Yellow pages

contact_gen takes a dataframe input with the links to websites in a column 'url', and changes it in place to remove unwanted links
    and links to potential listcles

selenium_scrape takes a link input and returns a tuple of email and phone numbers. if there are more than one, they are seperated
    by a whitespace 
"""


def contact_gen(serp):
    # regex pattern for weblinks
    link_pattern = 'https://[w]{3}\\.[a-zA-z0-9]+\\.(com)\\/?\\.?(sg)?\\/?'

    # Dropping all links that are likely blogs, listicles and product pages
    for index, lik1 in enumerate(serp['url']):
        if lik1.count('/', 0, len(lik1)) > 3:
            serp = serp.drop(index=index)

    serp = serp.reset_index()

    # Dropping all links that do not follow the regex pattern
    for index, lik2 in enumerate(serp['url']):
        if re.search(link_pattern, lik2) is None:
            serp = serp.drop(index=index)


def selenium_scrape(lk):
    driver_path = r'C:\Program Files (x86)\chromedriver.exe'
    e_pattern = '[a-zA-z0-9]+@[a-zA-z]+\\.[(com|sg)]+[\\.sg]*'
    p_pattern = '\\(?\\+?\\(?65\\)?\\)?\\s?\\(?[6|9|8][0-9]{3}\\s?[0-9]{4}\\)?'
    link_pattern = 'https://[w]{3}\\.[a-zA-z0-9]+\\.(com)\\/?\\.?(sg)?\\/?'
    driver = webdriver.Chrome(driver_path)
    email_list = []
    number_list = []

    # Getting the website, if not close and return 'Invalid URL'
    try:
        driver.get(lk)
        # Maximize the window so elements don't get lost
        driver.maximize_window()

    except WebDriverException:
        driver.close()
        return 'Invalid URL', 'Invalid URL'


    # Handling alerts that might pop up. If not, pass
    try:
        alert = driver.switch_to.alert
        alert.accept()

    except NoAlertPresentException:
        pass

    try:
        # First round of scraping; scraping the main web page
        source = driver.page_source
        [email_list.append(emails) for emails in re.findall(e_pattern, source)
         if emails not in email_list]
        [number_list.append(numbers) for numbers in re.findall(p_pattern, source)
         if numbers not in number_list]

        # Preparing to open and switch to tab window (Contact-Us Page)
        main_window = driver.current_window_handle
        tab_window = None

        # Finding a contact us page for the web
        try:
            # Trying to find via partial link text: Contact
            try:
                contact_us_list = driver.find_elements_by_partial_link_text('Contact')
                for contacts in contact_us_list:
                    if re.search(link_pattern, contacts.get_attribute('href')) is not None:
                        contacts.send_keys(Keys.CONTROL, Keys.RETURN)
                        break

            # If the link is found but not interactable, give the page some time to load, 5s
            except ElementNotInteractableException:
                time.sleep(5)
                contact_us_list = driver.find_elements_by_partial_link_text('Contact')
                for contacts in contact_us_list:
                    if re.search(link_pattern, contacts.get_attribute('href')) is not None:
                        contacts.send_keys(Keys.CONTROL, Keys.RETURN)
                        break

            # If there is no contact us link, try finding partial link text: About
            except NoSuchElementException:
                contact_us_list = driver.find_elements_by_partial_link_text('About')
                for contacts in contact_us_list:
                    if re.search(link_pattern, contacts.get_attribute('href')) is not None:
                        contacts.send_keys(Keys.CONTROL, Keys.RETURN)
                        break

        # If there is no contact or about us page, return the first round of scraping.
        except NoSuchElementException:
            driver.close()
            formatted_numbers = format(number_list)

            if len(email_list) >= 1:
                email_list = ' '.join(email_list)
            else:
                email_list = 'No Email'

            if len(formatted_numbers) >= 1:
                formatted_numbers = ' '.join(formatted_numbers)
            else:
                formatted_numbers = 'No Number'

            return email_list, formatted_numbers

        # Once the contact/about page is found, switch to the tab
        for DOM in driver.window_handles:
            if DOM != main_window:
                tab_window = DOM

        # Try switching to the tab window
        try:
            driver.switch_to.window(tab_window)

        # If that doesn't work, return the first round of scraping
        except InvalidArgumentException:
            driver.close()
            formatted_numbers = format(number_list)

            if len(email_list) >= 1:
                email_list = ' '.join(email_list)
            else:
                email_list = 'No Email'

            if len(formatted_numbers) >= 1:
                formatted_numbers = ' '.join(formatted_numbers)
            else:
                formatted_numbers = 'No Number'

            return email_list, formatted_numbers

        # Once swapped to the new tab, scrape the source code
        tab_source = driver.page_source
        [email_list.append(emails) for emails in re.findall(e_pattern, tab_source)
         if emails not in email_list]
        [number_list.append(numbers) for numbers in re.findall(p_pattern, tab_source)
         if numbers not in number_list]

        driver.close()
        driver.switch_to.window(main_window)
        driver.close()

        # Return the 2 rounds of scraping
        formatted_numbers = format(number_list)

        if len(email_list) >= 1:
            email_list = ' '.join(email_list)
        else:
            email_list = 'No Email'

        if len(formatted_numbers) >= 1:
            formatted_numbers = ' '.join(formatted_numbers)
        else:
            formatted_numbers = 'No Number'

        return email_list, formatted_numbers

    except WebDriverException:
        driver.close()
        return 'Invalid URL', 'Invalid URL'


def format(in_list):
    """Accepts a list of +65 Phone numbers and formats them to 8 digit numbers for local use"""
    formatted_numbers = []

    if len(in_list) > 0:
        for no in in_list:
            if len(no) > 8:
                unwanted = ['(', ')', '+', ' ']
                for symbol in unwanted:
                    if symbol in no:
                        no = no.replace(symbol, '')
                if no[0:2] == '65':
                    no = no[2:]
                
                if no not in formatted_numbers:
                    formatted_numbers.append(no)

    return formatted_numbers


if __name__ == '__main__':
    print("This file contains scrape, contact_gen and selenium_scrape")
    loop = True

    while loop:
        url = input("Which website would you like to scrape?: ")
        print(selenium_scrape(url))

        loop = input("Is there anything else? (y/n): ")
        loop = loop == 'y'
