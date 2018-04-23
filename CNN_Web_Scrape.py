import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from sys import platform


def init_browser():
    if platform == "darwin":
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    else:
        executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    
    nasa_data = {}
    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html    


    soup = BeautifulSoup(html, "html.parser")
    list_items = []
    list_items = soup.find_all(class_="item_list")
    titles = list_items[0].find_all("div", class_="content_title")

    title_list = []
    for div in titles:
        divs = div.text
        title_list.append(divs)
    
    teaser_soup = list_items[0].find_all("div", class_="article_teaser_body")
    
    teaser_list = []
    for teaser in teaser_soup:
        teasers = teaser.text
        teaser_list.append(teasers)

    nasa_data["title"] = title_list
    nasa_data["teasers"] = teaser_list
    
def build_titles(title):
    final_titles = ""
    for a in title:
        final_titles += " " + a.get_text()
        print(final_titles)
    return final_titles   


