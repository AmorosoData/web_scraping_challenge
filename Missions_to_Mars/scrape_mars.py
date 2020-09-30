# Importing dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # --- Visit Mars News site ---
    browser.visit('https://mars.nasa.gov/news/')

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the first news title
    news_title = soup.find("li", class_="slide").find("div", class_="content_title").text
    # Get the corresponding paragraph text
    news_p = soup.find("li", class_="slide").find("div", class_="article_teaser_body").text

    # --- Visit JPL site for featured Mars image ---
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    time.sleep(1)

    # Click through to full image
    browser.find_by_id('full_image')[0]
    featured_img_button.click()
    time.sleep(2)
    browser.is_element_present_by_text('more info',wait_time =2)
    browser.links.find_by_partial_text('more info').click()

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Search for image source
    featured_img = soup.select_one("figure.lede a img").get("src")
    featured_img = (f" https://www.jpl.nasa.gov{featured_img}")

    # --- Use Pandas to scrape Mars Space Facts ---
    mars_facts_url = pd.read_html("https://space-facts.com/mars/")

    table = pd.read_html(mars_facts_url)
    mars_df= table[0]

    mars_df.columns = ["Facts", "Measure"]
    # print(mars_df)
    
    # Convert table to html
    mars_table = mars_df.to_html(classes='data table', index=False, header=False, border=0)

    # --- Visit USGS Astrogeology Site ---
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    hemispheres = []

    # Search for the names of all four hemispheres
    results = soup.find_all('div',class_="collapsible results")
    hemi_list = results[0].find_all('h3')

    # Get text and store in list
    for name in hemi_list:
        hemispheres.append(name.text)

    # Search for thumbnail links
    thumbnail_results = results[0].find_all('a')
    thumbnails = []

    # Search for thumbnail links
    thumbnail_results = results[0].find_all('a')
    thumbnails = []

    for thumbnail in thumbnail_results:
    
        # If the thumbnail element has an image...
        if (thumbnail.img):
            # then grab the attached link
            thumbnail_url = 'https://astrogeology.usgs.gov/' + thumbnail['href']
            # Append list with links
            thumbnails.append(thumbnail_url)
    
    full_imgs = []

    for url in thumbnails:
    
        # Click through each thumbanil link
        browser.visit(url)
    
        html = browser.html
        soup = bs(html, 'html.parser')
    
        # Scrape each page for the relative image path
        results = soup.find_all('img', class_='wide-image')
        relative_img_path = results[0]['src']
    
        # Combine the reltaive image path to get the full url
        img_link = 'https://astrogeology.usgs.gov/' + relative_img_path
    
        # Add full image links to a list
        full_imgs.append(img_link)

    # Zip together the list of hemisphere names and hemisphere image links
    mars_hemi_zip = zip(hemispheres, full_imgs)

    hemisphere_image_urls = []

    # Iterate through the zipped object
    for title, img in mars_hemi_zip:
    
        mars_hemi_dict = {}
        
        # Add hemisphere title to dictionary
        mars_hemi_dict['title'] = title
        
        # Add image url to dictionary
        mars_hemi_dict['img_url'] = img
        
        # Append the list with dictionaries
        hemisphere_image_urls.append(mars_hemi_dict)
    
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_img,
        "mars_facts": mars_table,
        "hemispheres": hemisphere_image_urls
        }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
