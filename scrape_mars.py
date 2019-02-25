# Modules
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

# Initialize Splinter Browser
def initBrowser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
   

# Close Splinter Browser
def closeBrowser(browser):
    browser.quit()
    time.sleep(10)
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# Scrape
def scrape():
    mars_data = {}

    mars_data["news_data"] = marsNewsData()

    mars_data["mars_featured_image"] = marsFeaturedImage()

    mars_data["mars_weather"] = marsWeather()

    mars_data["mars_facts_table"] = marsFacts()

    mars_data["mars_hemispheres"] = marsHemisphereImages()

    return mars_data

# Mars News Data
def marsNewsData():
    news_data = {}

    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    time.sleep(5)

    soup = BeautifulSoup(response.text, 'html.parser')
    time.sleep(5)
    news_title=soup.find(class_="content_title").text
    news_title=news_title.strip('\n')
    news_p=soup.find(class_="rollover_description_inner").text
    news_p=news_p.strip('\n')

    news_data["news_title"]= news_title
    news_data["paragraph_text"]= news_p

    return news_data

# Mars Featured Image
def marsFeaturedImage():

    browser = initBrowser()    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(5)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    featured_image_url = browser.find_by_css('.fancybox-image').first['src']
    time.sleep(5)
    closeBrowser(browser)

    return featured_image_url

# Mars Weather Data
def marsWeather():

    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    time.sleep(5)

    soup = BeautifulSoup(response.text, 'html.parser')
    time.sleep(5)
    
    mars_weather_list = []
    for mars_weather in soup.find_all('p',class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        mars_weather_list.append(mars_weather.text.strip())

    mars_weather = mars_weather_list[2]

    return mars_weather

# Mars Facts
def marsFacts():

    url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(url)
    time.sleep(5)
    
    mars_facts_df = mars_facts[0]
    mars_facts_table = mars_facts_df.to_html(header=False, index=False)

    return mars_facts_table

# Mars Featured Image
def marsHemisphereImages():

    browser = initBrowser()
    time.sleep(5)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(5)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(5)
    
    first_product = browser.find_by_tag('h3')[0].text
    time.sleep(5)
    second_product = browser.find_by_tag('h3')[1].text
    time.sleep(5)
    third_product = browser.find_by_tag('h3')[2].text
    time.sleep(5)
    fourth_product = browser.find_by_tag('h3')[3].text
    time.sleep(5)

    
    browser.find_by_css('.thumb')[0].click()
    first_prod_img = browser.find_by_text('Sample')['href']
    browser.back()
    time.sleep(10)
    
    browser.find_by_css('.thumb')[1].click()
    second_prod_img = browser.find_by_text('Sample')['href']
    browser.back()
    time.sleep(10)

    browser.find_by_css('.thumb')[2].click()
    third_prod_img = browser.find_by_text('Sample')['href']
    browser.back()
    time.sleep(10)

    browser.find_by_css('.thumb')[3].click()
    fourth_prod_img = browser.find_by_text('Sample')['href']
    browser.back()
    time.sleep(10)

    mars_hemispheres=[{'title':first_product, 'hem_url': first_prod_img},
                       {'title':second_product,'hem_url': second_prod_img},
                       {'title':third_product, 'hem_url': third_prod_img},
                       {'title':fourth_product,'hem_url':fourth_prod_img}]
    
    closeBrowser(browser)
    time.sleep(10)

    return mars_hemispheres
