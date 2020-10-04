# Importing dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# --- Mars News ---
def scrape_mars_news():
    browser.visit('https://mars.nasa.gov/news/')
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Get the first news title
    news_title = soup.find("li", class_="slide").find("div", class_="content_title").text
    # Get the corresponding paragraph text
    news_p = soup.find("li", class_="slide").find("div", class_="article_teaser_body").text
    return news_title
    return news_p

def scrape_mars_img():
    # --- Visit JPL site for featured Mars image ---
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    time.sleep(1)
    # Click through to full image
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
    return featured_img_url

def scrape_mars_table():
    # --- Use Pandas to scrape Mars Space Facts ---
    mars_facts_url = pd.read_html("https://space-facts.com/mars/")
    mars_table = pd.read_html(mars_facts_url)
    # mars_table= table[0]

    # mars_table.columns = ["Facts", "Measure"]
    # mars_table.to_html(classes = "table table-striped")
    return mars_table

    
def scrape_hemispheres():
    # --- Visit USGS Astrogeology Site ---
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    base_url = "https://astrogeology.usgs.gov"
    hemispheres = soup.find("div", class_ = "collapsible").find_all("div", class_="item")
    
    print("======================")
    hemisphere_list = []
    title_list = []
    # print(hemispheres)
    for hemisphere in hemispheres:
      
        browser.visit(base_url+hemisphere.find("a").get("href"))
        html = browser.html
        soup = bs(html, 'html.parser')
        img = soup.select_one("li a").get("href")
        # hemisphere_list.append(img)
        title = soup.find("h2", class_ = "title").text
        # title_list.append(title)

        hemisphere_dict = {
            "img_url":img,"title": title
        }
        hemisphere_list.append(hemisphere_dict)
        print(hemisphere_list)

scrape_hemispheres()
browser.quit()


    # # Store data in a dictionary
    # mars_data = {
    #     "news_title": news_title,
    #     "news_paragraph": news_p,
    #     "featured_image": featured_img,
    #     "mars_facts": mars_table,
    #     "hemispheres": hemisphere_image_urls
    #     }

    # # Close the browser after scraping
    # browser.quit()

    # # Return results
    # return mars_data
