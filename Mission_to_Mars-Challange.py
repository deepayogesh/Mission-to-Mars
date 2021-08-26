#!/usr/bin/env python
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)     #  headless set to FALSE because we were running in Jupyter notebook and want to see scraping
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)
#  set up HTML parser 
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')              #slide_elem  is avariable which will look for div tag   This is our parent element
#  looking for a <div /> with a class of “content_title.”
slide_elem.find('div', class_='content_title')
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

#  set up our browser for this new url 

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)
#  # Find and click the full image button
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


# # Scrape Mars Data: Mars Facts

#  Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
# By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. 
#  Then, it turns the table into a DataFrame
df = pd.read_html('https://galaxyfacts-mars.com')[0]    #    creating a new DataFrame from the HTML table. The Pandas function read_html()
df.columns=['description', 'Mars', 'Earth']                      #   assign columns to the new DataFrame for additional clarity
df.set_index('description', inplace=True)                     #   using the .set_index() function, we're turning the Description column into the DataFrame's index. inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable
#  Convert this dataframe table to HTML 
df.to_html()
browser.quit()     #  end the browser session you created 

# # Visit the NASA Mars News Site

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[19]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[20]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[21]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[22]:


slide_elem.find('div', class_='content_title')


# In[23]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[24]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[25]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[26]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[27]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[28]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[29]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # Mars Facts

# In[30]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[31]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[32]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 

url = 'https://marshemispheres.com/'
browser.visit(url)
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(4):
    # Dicttionary to hold the titles and image url for each image 
    dict_hemispheres = {}
    browser.find_by_css('a.product-item h3')[i].click()
    element = browser.find_link_by_text('Sample').first
    img_url = element['href']
    title = browser.find_by_css("h2.title").text
    dict_hemispheres["img_url"] = img_url
    dict_hemispheres["title"] = title
    hemisphere_image_urls.append(hemispheres_dict)  # add this to our list 
    browser.back() # will go back to first page
# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)

# 5. Quit the browser
browser.quit()

