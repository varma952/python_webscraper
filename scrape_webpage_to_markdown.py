import json
import time

import requests
from bs4 import BeautifulSoup
from langchain_community.document_transformers import MarkdownifyTransformer
from langchain_core.documents import Document
from selenium import webdriver
from selenium.webdriver.common.by import By

processed_links = []
metadata = {}


def load_webdriver():

    # set up ChromeOptions
    options = webdriver.ChromeOptions()

    # add headless Chrome option
    options.add_argument("--headless=new")

    # set up Chrome in headless mode
    driver_client = webdriver.Chrome(options=options)

    return driver_client

def download_documents(link: str):
    response = requests.get(link)
    file_name = link.rsplit("/", 1)[1]
    with open(f"./documents/{file_name}", mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)
    metadata[file_name] = link

def process_webpage(document_str: str, link: str):
    docs = [Document(page_content=document_str, metadata={"source": link})]
    md = MarkdownifyTransformer()
    converted_docs = md.transform_documents(docs)
    file_name = link.rsplit("/", 1)[1].rsplit(".html", 1)[0]
    with open(f"./documents/{file_name}.md", "w", encoding="UTF-8") as f:
        f.write(converted_docs[0].page_content)

    metadata[file_name] = link


def link_filters(links: list) -> list:
    filtered_links = [link["href"] for link in links if "www.shell.com" in link["href"]]
    filtered_links = list(set(filtered_links))
    final_links = []
    for link in filtered_links:
        if (
            "sustainability" in link
            or "environment" in link
            or "esg" in link
            or "social" in link
            or "human" in link
        ):
            final_links.append(link)
    return final_links


def start_scrapping(driver_client, parent_link: str):
    if not parent_link in processed_links:
        driver_client.get(parent_link)
        time.sleep(5)
        print(f"Working on link {parent_link}")
        if parent_link.endswith(".html"):
            content = driver_client.page_source
            process_webpage(content, parent_link)
            # Read content to links
            soup = BeautifulSoup(content, "html.parser")
            links = soup.find_all("a", href=True)
            processed_links.append(parent_link)
            for link in link_filters(links):
                start_scrapping(driver_client, link)
        else:
            download_documents(parent_link)
            processed_links.append(parent_link)
        

driver = load_webdriver()
esg_parent_link = (
    "https://www.shell.com/investors/environmental-social-and-governance.html"
)
start_scrapping(driver, esg_parent_link)

with open('./documents/metadata.json', 'w', encoding='utf-8') as f:
    json.dump(metadata, f)