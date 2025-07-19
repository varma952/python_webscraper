from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import requests

processed_links = []

def load_webdriver():

    # set up ChromeOptions
    options = webdriver.ChromeOptions()

    # add headless Chrome option
    options.add_argument("--headless=new")

    # set up Chrome in headless mode
    driver_client = webdriver.Chrome(options=options)

    return driver_client

# define a function to get scroll dimensions
def get_scroll_dimension(axis: str):
    return driver.execute_script(f"return document.body.parentNode.scroll{axis}")

def download_documents(link:str):
    response = requests.get(link)
    file_name = link.rsplit("/",1)[1]
    with open(f"./documents/{file_name}", mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)

def printscreen_webbpage(driver_client, link:str):
    # get the page scroll dimensions
    width = get_scroll_dimension("Width")
    height = get_scroll_dimension("Height")

    # set the browser window size
    driver_client.set_window_size(width, height)

    # get the full body element
    full_body_element = driver_client.find_element(By.TAG_NAME, "body")

    # take a full-page screenshot
    file_name = link.rsplit("/",1)[1].rsplit(".html",1)[0]
    full_body_element.screenshot(f"screenshots/{file_name}.png")
    processed_links.append(link)

def link_filters(links:list) -> list:
    filtered_links = [link["href"] for link in links if "www.shell.com" in link["href"]]
    filtered_links = list(set(filtered_links)) 
    final_links = []
    for link in filtered_links:
        if ("sustainability" in link or "environment" in link or "esg" in link or "social" in link or "human" in link):
            final_links.append(link)
    return final_links

def start_scrapping(driver_client, parent_link: str):
    if not parent_link in processed_links:
        driver_client.get(parent_link)
        time.sleep(5)
        print(f"Working on link {parent_link}")
        if parent_link.endswith(".html"):
            printscreen_webbpage(driver_client,parent_link)
        else:
            download_documents(parent_link)

        # Read content to links
        content = driver_client.page_source
        soup = BeautifulSoup(content, "html.parser")
        links = soup.find_all("a",href=True)

        for link in link_filters(links):
            start_scrapping(driver_client, link)

driver = load_webdriver()
esg_parent_link = "https://www.shell.com/investors/environmental-social-and-governance.html"
start_scrapping(driver, esg_parent_link)

