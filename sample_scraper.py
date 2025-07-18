from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

import re

def load_webdriver():

    # set up ChromeOptions
    options = webdriver.ChromeOptions()

    # add headless Chrome option
    options.add_argument("--headless=new")

    # set up Chrome in headless mode
    driver = webdriver.Chrome(options=options)

    return driver

# define a function to get scroll dimensions
def get_scroll_dimension(axis):
    return driver.execute_script(f"return document.body.parentNode.scroll{axis}")




driver = load_webdriver()
# open the target website
driver.get("https://www.shell.com/investors/environmental-social-and-governance.html")
time.sleep(10)



# get the page scroll dimensions
width = get_scroll_dimension("Width")
height = get_scroll_dimension("Height")

# set the browser window size
driver.set_window_size(width, height)

# get the full body element
full_body_element = driver.find_element(By.TAG_NAME, "body")

# take a full-page screenshot
full_body_element.screenshot("screenshots/selenium-full-page-screenshot.png")
content = driver.page_source

soup = BeautifulSoup(content, "html.parser")
links = []
web_text = ""
links = links+soup.find_all("a",href=True)
links = [link["href"] for link in links if "www.shell.com" in link["href"]]
links = list(set(links))
list(set(links))
for link in links:
    if "sustainability" in link or "environment" in link or "esg" in link or "social" in link or "human" in link:
        driver.get(link)
        soup_text = BeautifulSoup(driver.page_source, "html.parser")
        time.sleep(2)
        web_text = web_text+soup_text.text
        print(web_text)

# close the driver instance and release its resources
driver.quit()