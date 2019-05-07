from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

def init_browser():
    executable_path = {'executable_path': 'C:/Users/Admin/Downloads/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()
    mars_data = {}

    page = requests.get("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")
    soup = BeautifulSoup(page.content, 'html.parser')

    article=soup.find("div", class_="image_and_description_container")
    article_items=article.find_all("img")
    item=article_items[1]
    news_title=item["alt"]
    news_p=article.find("div", class_="rollover_description_inner").get_text()

    mars_data["news_headline"] = news_title
    mars_data["news_paragraph"] = news_p
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find("img", class_="thumb")["src"]
    featured_image_url =f"https://jpl.nasa.gov{img}"

    mars_data["latest_image"]=featured_image_url

    page_mars = requests.get("https://twitter.com/marswxreport?lang=en")
    soup_mars = BeautifulSoup(page_mars.content, 'html.parser')

    get_tweet=soup_mars.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0]
    mars_weather=get_tweet.get_text()
    mars_data["weather"]=mars_weather
 
    
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
   
     
    df=tables[0]
    df.columns=['Mars Facts','Data']
    

    html_table = df.to_html()
    html_table.replace('\n', '')

    mars_data["table"]=html_table

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls=[]
    titles=soup.find_all("h3")
    imgs=soup.find_all("img", class_="thumb")
    img= [("https://astrogeology.usgs.gov" + i["src"]) for i in imgs]
    title = [(t.get_text()) for t in titles]
    hemisphere_image_urls = []

    for i in range(len(title)):
        dict1={}
        dict1["title"] = title[i]
        dict1["img_url"] = img[i]
        hemisphere_image_urls.append(dict1)

    mars_data["hemisphere_imgs"]=hemisphere_image_urls
    print(mars_data)
    return mars_data

if __name__ == '__main__':
    scrape()