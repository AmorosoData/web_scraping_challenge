# Importing dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    # This is my path to chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# --- Mars News ---
def scrape():
    browser = init_browser()
    mars_info = {}

    news_url = ('https://mars.nasa.gov/news/')
    browser.visit(news_url)

    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    mars_info['title'] = soup.find("li", class_="slide").find("div", class_="content_title").text
    mars_info['paragraph']= soup.find("li", class_="slide").find("div", class_="article_teaser_body").text
    
    # mars_info = {
    #     'news_title': news_title,
    #     'news_paragraph': news_p
    #     }
    
    # news_title = soup.find("li", class_="slide").find("div", class_="content_title").text
    # news_p = soup.find("li", class_="slide").find("div", class_="article_teaser_body").text
    
    # mars_info = {
    #         'news_title': news_title,
    #         'news_paragraph': news_p
    #     }
    return mars_info

# # --- Visit JPL site for featured Mars image ---
# def scrape_mars_img():
#     browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
#     time.sleep(1)
 
#     featured_img_button = browser.find_by_id('full_image')[0]
#     featured_img_button.click()
#     browser.is_element_present_by_text('more info',wait_time =2)
#     more_info_button = browser.links.find_by_partial_text('more info')
#     more_info_button.click()

#     # Scrape page into Soup
#     html = browser.html
#     soup = bs(html, 'html.parser')

#     # Search for image source
#     featured_img = soup.select_one("figure.lede a img").get("src")
#     featured_img_url = (f" https://www.jpl.nasa.gov{featured_img}")
#     return featured_img_url

# # --- Use Pandas to scrape Mars Space Facts ---
# def scrape_mars_table():
#     facts_url = pd.read_html("https://space-facts.com/mars/")
#     mars_table = pd.read_html(facts_url)
#     return mars_table

# # --- Visit USGS Astrogeology Site ---  
# def scrape_hemispheres():
#     browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
#     time.sleep(1)

#     html = browser.html
#     soup = bs(html, 'html.parser')

#     base_url = "https://astrogeology.usgs.gov"
#     hemispheres = soup.find("div", class_ = "collapsible").find_all("div", class_="item")
#     # print(hemispheres)
#     # print("======================")
#     hemisphere_list = []
#     title_list = []

#     for hemisphere in hemispheres:
#         browser.visit(base_url+hemisphere.find("a").get("href"))
#         html = browser.html
#         soup = bs(html, 'html.parser')
#         img = soup.select_one("li a").get("href")
#         # hemisphere_list.append(img)
#         title = soup.find("h2", class_ = "title").text
#         # title_list.append(title)

#         hemisphere_dict = {
#             "img_url":img,"title": title
#         }
#         hemisphere_list.append(hemisphere_dict)
#         return hemisphere_dict

#         browser.quit()
        

    # return mars_data
