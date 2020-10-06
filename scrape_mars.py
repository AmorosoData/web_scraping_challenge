# Importing dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests

def init_browser():
    # This is my path to chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# --------------------- Mars News --------------------------
def scrape_mars_news():
    try:
        browser = init_browser()
        url = ('https://mars.nasa.gov/news/')
        browser.visit(url)
        # time.sleep(1)
        html = browser.html
        soup = bs(html, "html.parser")

        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p
        return mars_info
    # mars_info = {
    #     'news_title': news_title,
    #     'news_paragraph': news_p
    #     }
    
    # news_title = soup.find("li", class_="slide").find("div", class_="content_title").text
    # news_p = soup.find("li", class_="slide").find("div", class_="article_teaser_body").text
    finally:
        browser.quit()

# ------------------ Visit JPL site for featured Mars image ----------------------------
def scrape_mars_image():
    try:
        browser = init_browser()

        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)# Visit Mars Space Images through splinter module
 
        featured_img_button = browser.find_by_id('full_image')[0]
        featured_img_button.click()

        browser.is_element_present_by_text('more info',wait_time =2)
        more_info_button = browser.links.find_by_partial_text('more info')
        more_info_button.click()

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, 'html.parser')

        # Search for image source
        featured_img = soup.select_one("figure.lede a img").get("src")
        featured_image_url = (f" https://www.jpl.nasa.gov{featured_img}")
        featured_image_url
        
        mars_info['featured_image_url'] = featured_image_url

        return mars_info
    finally:
        browser.quit()

# ----------------------------- Mars Facts ---------------------------------
def scrape_mars_facts():

    facts_url = 'http://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)

    mars_df = mars_facts[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = data

    return mars_info

# ------------------------- MARS HEMISPHERES ---------------------------

def scrape_mars_hemispheres():
    try: 
        browser = init_browser()
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        html_hemispheres = browser.html
        soup = bs(html_hemispheres, 'html.parser')
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemi = []
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            title = i.find('h3').text
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(hemispheres_main_url + partial_img_url)
            partial_img_html = browser.html
            soup = bs( partial_img_html, 'html.parser')
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemi.append({"title" : title, "img_url" : img_url})

        mars_info['hemi'] = hemi
        return mars_info
    finally:
        browser.quit()
