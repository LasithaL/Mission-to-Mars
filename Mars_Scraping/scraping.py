# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    # Setup Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    featured_image(browser)
    mars_facts()
    hemisphere_image_urls(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try.except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None

    return news_title, news_p


# ### JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url


# ### Scraping the Tabular Data from Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # use read_html to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
        
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
def hemisphere_image_urls(browser):
    # Visit the url
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
    try:
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
    except BaseException:
        return None

    # 4. Print the list that holds the dictionary of each image url and title.
    #print(hemisphere_image_urls)
    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

