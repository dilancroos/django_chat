from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
# from a_rtchat.views import msg

from bs4 import BeautifulSoup
import requests
import json
import os


def get_data(msg):
    chrome_options = webdriver.ChromeOptions()
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isHeaderFooterEnabled": False
    }
    download_directory = os.path.join(os.getcwd(), "data")
    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': download_directory
    }

    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    driver.get("https://www.ft.com/search")  # https://www.bloomberg.com/search
    driver.implicitly_wait(5)

    print("Page title: ", driver.title)

    iframe = None

    # Find the cookie iframe

    def find_iframe(driver):
        try:
            iframe = driver.find_element(
                By.ID, "sp_message_iframe_1098749")  # id="sp_message_iframe_1036083"
        except:
            print("try did not work")

        try:
            iframe = driver.find_element(
                By.ID, "sp_message_iframe_1098748")
        except:
            print("except")

        driver.switch_to.frame(iframe)

        print("switched to iframe")

        try:
            # Wait for the accept cookies button to be clickable
            accept_button = driver.find_element(
                # /html/body/div/div[2]/div[5]/button[2]
                By.XPATH, '/html/body/div/div[2]/div[3]/div/button[2]')

            # Click the accept cookies button
            accept_button.click()
            print("Accept cookies button clicked")

            driver.switch_to.default_content()  # Switch back to the main page

        except TimeoutException:
            print("Timeout: Accept cookies button not found within the specified time")

        return

    find_iframe(driver)

    # Continue with your scraping or other actions
    driver.find_element(
        # '//*[@id="root"]/div/section[1]/div[1]/div[2]/div/input'
        By.CLASS_NAME, "search-head__form-submit-wrapper").find_element(By.NAME, "q")

    print("input_element found")

    driver.find_element(
        # '//*[@id="root"]/div/section[1]/div[1]/div[2]/div/input'
        By.CLASS_NAME, "search-head__form-submit-wrapper").find_element(By.NAME, "q").send_keys(msg)

    print("Search input sent")

    driver.find_element(
        By.CLASS_NAME, "search-head__form-submit-wrapper").find_element(By.NAME, "q").send_keys(Keys.RETURN)

    print("Search Enter sent")

    time.sleep(3)
    # Wait for the search results to load

    try:
        find_iframe(driver)
    except:
        print("iframe not found")

    print("Page title: ", driver.title)

    # get first 3 search results
    search_results = driver.find_elements(
        By.CLASS_NAME, "js-teaser-heading-link")

    n = 0
    link_list = []

    for i, result in enumerate(search_results[:20]):

        links = requests.get(result.get_attribute('href'))
        link_pages = BeautifulSoup(links.content, "html.parser")

        page_limited_a = link_pages.find_all(
            'a', attrs={'id': 'charge-button'})

        if page_limited_a:
            continue
        elif n > 3:
            break
        else:
            n += 1
            print(f"Result {i+1}: {result.get_attribute('href')}")
            link_list.append(result.get_attribute('href'))

    for i, link in enumerate(link_list):
        driver.get(link)

        driver.implicitly_wait(3)

        try:
            driver.find_element(By.CLASS_NAME, "o-banner__close").click()
        except:
            print("Banner not found")

        time.sleep(3)

        try:
            driver.execute_script('window.print();')
        except:
            print("Print not working")

        print(f"Page {i+1} title: {driver.title}")

    # Remember to close the browser
    driver.quit()

    return
