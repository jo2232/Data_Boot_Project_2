import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from sys import platform

def scrape_it():
    def init_browser():
        if platform == "darwin":
            executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        else:
            executable_path = {'executable_path': 'chromedriver.exe'}
        return Browser("chrome", **executable_path, headless=False)


    city_list = ["Atlanta", "Chicago", "Dallas", "Las Vegas", "Los Angeles", "Kansas City", "Miami", "New York", "Seattle", "St. Louis"]
    browser = init_browser()

    for city in city_list:
        article_list = []
        url = 'https://www.cnn.com/search?size=10&q=' + city
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser') 
        articles = soup.find_all('div', class_="cnn-search__result--article")

        for headline in articles:
            title = headline.find("h3", class_="cnn-search__result-headline")
            link = title.find("a")
            article_list.append(link)
        
        links = [a.get('href') for a in article_list]
        article_headlines = [b.get_text() for b in article_list]
    
        city_for_dict = []
        for i in range(0, len(links)):
            city_for_dict.append(city)
   
        cnn_data = []
        for i in range(0, len(links)):
            item = { "headline": article_headlines[i],
                "links": links[i],
                "city": city_for_dict[i]}
            cnn_data.append(item)
    return(cnn_data)