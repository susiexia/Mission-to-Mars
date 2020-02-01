# %%
from splinter import Browser
from bs4 import BeautifulSoup

# %%
# initial auto browser
browser = Browser('chrome', executable_path='chromedriver.exe',headless=False)

# %% [markdown]
# ## Web Scrape the latest news from NASA Mars news website
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

# %%
image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
