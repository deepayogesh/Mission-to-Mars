#Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import pandas as pd
def scrape_all():
    # Initiate headless Driver for Deployement   set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    hemispheres =[]

    # Run all scraping functions 
    data = {
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image": featured_image(browser),
        "facts":mars_facts(),
        "last_modified":dt.datetime.now(),
        "hemispheres":mars_hemispheres(browser)
    }

    # Stop Webdriver and return data 
    browser.quit()
    return data

def mars_news(browser):
    #Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    #Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    #set up HTML parser 
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')              #slide_elem  is avariable which will look for div tag   This is our parent element
    #looking for a <div /> with a class of “content_title.”
    slide_elem.find('div', class_='content_title')
    #Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_title
    #Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p
##Scrape Mars Data: Featured Image
def featured_image(browser):
    # Visit URL 
    url= 'https://spaceimages-mars.com'
    browser.visit(url)
    ## Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Add try /except for error handling 
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url
def mars_facts():
    #Add try /except for Error Handling 
    try: 
        # Use 'read_html' to scrape the facts table into  dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    # Assign Columns and set Index of dataframe 
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    # Convert dataframe into HTML format ,add bootstrap
    return df.to_html()

def mars_hemispheres(browser):
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
        try:
            img_url = element['href']
            title = browser.find_by_css("h2.title").text
        except AttributeError:
            return None
            
        dict_hemispheres["img_url"] = img_url
        dict_hemispheres["title"] = title
        hemisphere_image_urls.append(dict_hemispheres)  # add this to our list 
        browser.back() # will go back to first page
    # 4. Print the list that holds the dictionary of each image url and title.
    #print(hemisphere_image_urls)
    # 5. Quit the browser
    #browser.quit()
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

