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

    return mars_info
finally:
    browser.quit()

# ------------------ Visit JPL site for featured Mars image ----------------------------
def scrape_mars_image():
    try:
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
        featured_img_url = (f" https://www.jpl.nasa.gov{featured_img}")
        featured_img_url
        
        mars_info['featured_image_url'] = featured_image_url

        return mars_info
    finally:
        browser.quit()

# ------------------- Use Pandas to scrape Mars Space Facts ----------------------

# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 

    exec_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    return Browser('chrome', headless=True, **exec_path)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("div.content_title", wait_time=1)

        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')


        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

# FEATURED IMAGE
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)# Visit Mars Space Images through splinter module

        # HTML Object 
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve background-image url from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scrapped route
        featured_image_url = main_url + featured_image_url

        # Display full link to featured image
        featured_image_url 

        # Dictionary entry from FEATURED IMAGE
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

# ------------------------------ Visit USGS Astrogeology Site --------------------  
def scrape_mars_hemispheres():
    try: 
        browser = init_browser()
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemi = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemi.append({"title" : title, "img_url" : img_url})

        mars_info['hemi'] = hemi

        return mars_info
    finally:

        browser.quit()
