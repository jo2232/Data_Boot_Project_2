import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from sys import platform


# In[2]:

def scrape_it():
    def init_browser():
        if platform == "darwin":
            executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        else:
            executable_path = {'executable_path': 'chromedriver.exe'}
        return Browser("chrome", **executable_path, headless=False)


    # In[21]:



    browser = init_browser()
        
    article_list = []
        
    url = 'https://www.cnn.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser') 

    input_field = browser.find_by_css('#searchInputFooter')
    input_field[0].fill('dallas')
    search_button = browser.find_by_xpath('/html/body/footer/div[1]/div[2]/form/button').first
    search_button.click()
    time.sleep(7)

    html = browser.html
    # create soup object from html
    article_soup = BeautifulSoup(html, "html.parser")
    articles = article_soup.find_all(class_="cnn-search__result--article")
    for headline in articles:
        title = headline.find("h3", class_="cnn-search__result-headline")
        link = title.find("a")
        article_list.append(link)
        
    links = [a.get('href') for a in article_list]
    article_headlines = [b.get_text() for b in article_list]
    print(links)
    print(article_headlines)

    article_dict = {'headline':[], 'link':[]}
    for i in range(0,len(links)):
        article_dict['headline'].append(article_headlines[i])
        article_dict['link'].append(links.[i])
    
    return article_dict