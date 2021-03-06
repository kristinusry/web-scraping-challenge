from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    
    # LATEST MARS NEWS
    #-------------------------------------------------
    # Open Nasa Mars website
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get latest new title and description
    news_title = soup.select_one('ul.item_list li.slide div.content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # LATEST MARS IMAGE
    #-------------------------------------------------
    # Open Nasa images website to Mars category
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    image_root = 'https://www.jpl.nasa.gov'
    browser.visit(image_url)
    time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get featured image URL
    relative_image_path = soup.find_all('img')[3]["src"]
    featured_image_url = image_root + relative_image_path

    # LATEST MARS WEATHER FROM TWITTER
    #-------------------------------------------------
    # Open Mars weather twitter
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find all elements that contain tweets
    tweets = soup.find_all('span', text=re.compile('InSight sol'))
    latestweather = tweets[0].get_text()
    
    # LATEST MARS FACTS
    #-------------------------------------------------
    # Open space-facts for Mars
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    html = browser.html

    # Use Pandas to scrape the table containing facts about Mars
    table = pd.read_html(facts_url)
    mars_facts = table[0]

    # Rename columns and set index
    mars_facts.columns = ['Description','Value']
    mars_facts.set_index('Description', inplace=True)
    
    # Convert to HTML table string
    mars_facts = mars_facts.to_html(classes="table table-striped")

    # MARS HEMISPHERES
    #-------------------------------------------------
    # Open Cerberus
    cerberus_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    browser.visit(cerberus_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get featured image URL
    cerberus = soup.select_one('div.downloads a')['href']

    # Open schiaparelli
    schiaparelli_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    browser.visit(schiaparelli_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get featured image URL
    schiaparelli = soup.select_one('div.downloads a')['href']

    # Open syrtis
    syrtis_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    browser.visit(syrtis_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get featured image URL
    syrtis = soup.select_one('div.downloads a')['href']

    # Open Valles Marieneris
    valles_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    browser.visit(valles_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get featured image URL
    valles = soup.select_one('div.downloads a')['href'] 

    # Create a list of Mars Hemisphere images
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": valles},
        {"title": "Cerberus Hemisphere", "img_url": cerberus},
        {"title": "Schiaparelli Hemisphere", "img_url": schiaparelli},
        {"title": "Syrtis Major Hemisphere", "img_url": syrtis},
    ]

    #-------------------------------------------------   
    # STORE ALL SCRAPED DATA INTO DICTIONARY
    #-------------------------------------------------
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": mars_facts,
        "latestweather": latestweather,
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_data