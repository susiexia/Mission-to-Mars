
from splinter import Browser
from bs4 import BeautifulSoup

import pandas
import datetime as dt 

# -------------------------------------------------------
# an integrat function
def scrape_all():

    # initial headless driver for deployment
    browser = Browser('chrome', executable_path='chromedriver.exe',headless=False)

    # ------------------------Challenge-----------------------------
    # store hemisphere data as a list of dictionaries, one dictionary for each hemisphere data.
    mars_hemi_lst = list()
    names = ['Cerberus','Schiaparelli', 'Syrtis Major','Valles Marineris']
    for name in names:
        # call scraping fuction for each hemisphere
        hemi_title, hemi_img_url = mars_hemispheres(browser, name)
       # add scraped data into dictionary
        hemi_dict = {"img_url":hemi_img_url, "title": hemi_title}
        # add each dictionary into list
        mars_hemi_lst.append(hemi_dict)
    
    # run all scraping funtions, and store results in dictionary structure
    news_title, news_paragraph = mars_news(browser)

    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemi_data": mars_hemi_lst}


    browser.quit()

    return data




# ------------------Chellenge-------------------------------------

# hemi_name: Cerberus, Schiaparelli, Syrtis Major, Valles Marineris
def mars_hemispheres(browser, hemi_name):

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    # STEP 1: click '... Hemisphere Enhanced'button
    browser.is_element_present_by_text(f'{hemi_name} Hemisphere Enhanced', wait_time = 1)
    browser.click_link_by_partial_text(f'{hemi_name} Hemisphere Enhanced')
    
    # STEP 2: BeautifulSoup to parse and extract image url
    soup = BeautifulSoup(browser.html, 'html.parser')
    try:
        rel_url = soup.select_one('img.wide-image').get('src')
        title = soup.select_one('h2.title').text
    except AttributeError:
        return None
    # STEP 3: combine as an absolute url
    img_url = f'https://astrogeology.usgs.gov{rel_url}'
    
    return title, img_url


# ----------------------------------------------------------------
# ## Web Scrape the latest news from NASA Mars news website
# - (auto visit a website to extract string results)

def mars_news(browser):
    # use browser auto visit Mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # delay 1 second for loading the page
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

    # use BeautifulSoup to parse an html file
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # parse html and extract the most recently news as parent element
        slide_parent_elem = soup.select_one('ul.item_list li.slide')
        #use parent element to extract news' title
        news_title = slide_parent_elem.find('div', class_='content_title').get_text()
        # use parent element to extract news' summary
        news_p = slide_parent_elem.select_one('div.article_teaser_body').text
    except AttributeError:
        return None, None

    return news_title, news_p

# -----------------------------------------------------------------
# ## Web Scrape the Featured Images from NASA Mars spaceimages website

def featured_image(browser):
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # STEP 1: click by id = 'full_image' and assign to a variable
    full_image_elem = browser.find_by_id('full_image', wait_time=1)
    full_image_elem.click()

    # STEP 2: click by text 'more info' and assign to a variable
    browser.is_element_present_by_text('more info', wait_time=1) # make sure if text in page
    browser.click_link_by_partial_text('more info')

    # STEP 3:use BeautifulSoup to parse 
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    # use CSS selector in BeautifulSoup to extract img_url
    try:
        image_relative_url = image_soup.select_one('figure.lede a img').get('src')
    except AttributeError:
        return None
    #combine with base URL to create an absolute img URL
    img_url = f'https://www.jpl.nasa.gov{image_relative_url}'
    
    return img_url


# ------------------------------------------------------------------
# ## Web Scrape TABLE from Mars facts website

def mars_facts():

    fact_url = 'http://space-facts.com/mars/' 
    try:
        # extract the first one in list of DFs
        df = pandas.read_html(fact_url)[0]
    except BaseException:
        return None

    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    
    return df.to_html(classes="table table-striped")


# in case run this as python script
if __name__ == "__main__":
    print(scrape_all())