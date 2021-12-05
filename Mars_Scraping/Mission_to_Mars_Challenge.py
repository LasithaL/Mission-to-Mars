#!/usr/bin/env python
# coding: utf-8


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## Article Scraping form redplanetscience.com


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Scraping the Tabular Data from Mars Facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Parse the data
title_html = browser.html
title_soup = soup(title_html, 'html.parser')

# Retrieve all items in Products section
items = title_soup.find_all('div', class_='item')

# Scrape through all items
for item in items:
    hemi_data = {}
    
    # Extract title
    title = item.find('h3').text
    
    # Extract image url through a reference url
    # Create a reference url
    ref_url = item.find('a', class_='itemLink product-item')['href']
    # Visit the the reference url
    new_url = f'{url}{ref_url}'
    browser.visit(new_url)
    # Parse the new data
    new_html = browser.html
    new_soup = soup(new_html, 'html.parser')
    # Find the image pointer
    img_download = new_soup.find_all('li')
    pointer_url = img_download[0].find('a')['href']
    img_url = f'{url}{pointer_url}'
    
    #print(title)
    #print(img_url)
    
    # Add title and image url to the dictionary
    hemi_data = {
        'img_url': img_url,
        'title': title
    }
    
    # Append the list
    hemisphere_image_urls.append(hemi_data)
    
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()
