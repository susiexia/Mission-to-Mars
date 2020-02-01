# %%
from splinter import Browser
from bs4 import BeautifulSoup

import pandas
# %%
# initial auto browser
browser = Browser('chrome', executable_path='chromedriver.exe',headless=False)

# %% [markdown]
# ## Web Scrape the latest news from NASA Mars news website
# - (auto visit a website to extract string results)
# %%
# use browser auto visit Mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# delay 1 second for loading the page
browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

# %%
# use BeautifulSoup to parse an html file
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# parse html and extract the most recently news as parent element
slide_parent_elem = soup.select_one('ul.item_list li.slide')
#use parent element to extract news' title
news_title = slide_parent_elem.find('div', class_='content_title').get_text()
# use parent element to extract news' summary
news_p = slide_parent_elem.select_one('div.article_teaser_body').text

news_title
news_p
# %% [markdown]
# ## Web Scrape the Featured Images from NASA Mars spaceimages website
# - (navigate brower through links to extract img_url)
# %%
# use browser auto visit SpaceImage website
image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(image_url)

# directly use browser functions, not transfer to html now.

# STEP 1: click by id = 'full_image' and assign to a variable
full_image_elem = browser.find_by_id('full_image', wait_time=1)
full_image_elem.click()

# STEP 2: click by text 'more info' and assign to a variable
browser.is_element_present_by_text('more info', wait_time=1) # make sure if text in page
more_info_elem = browser.click_link_by_partial_text('more info')

# STEP 3:use BeautifulSoup to parse 
html = browser.html
image_soup = BeautifulSoup(html, 'html.parser')
# use CSS selector in BeautifulSoup to extract img_url
image_relative_url = image_soup.select_one('figure.lede a img').get('src')

#combine with base URL to create an absolute img URL
img_url = f'https://www.jpl.nasa.gov{image_relative_url}'
img_url

# check if a valid img_url
#browser.visit(img_url)
# %% [markdown]
# ## Web Scrape TABLE from Mars facts website
# - (use Pandas funtions to parse HTML Table)
# - (No BeautifulSoup used)
# - (No auto browser used)
# %%
fact_url = 'http://space-facts.com/mars/' # only accept http without s
# extract the first one in list of DFs
df = pandas.read_html(fact_url)[0]
df.columns = ['description', 'value']
df.set_index('description', inplace=True)
df
# convert back to HTML string
fact_table_html = df.to_html()
fact_table_html
# %%
browser.quit()

# %%
