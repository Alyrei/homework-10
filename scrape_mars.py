from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_library = {}

    ############### Mars News ###############

    # Website to be scraped
    url1 = "https://mars.nasa.gov/news/"
    browser.visit(url1)
    html = browser.html
    soup = bs(html, 'html.parser')
    # Assign the most recent article, title, paragraph and date
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
    # Add to dictionary
    mars_library["news_date"] = news_date
    mars_library["news_title"] = news_title
    mars_library["summary"] = news_p

    ############### Image Search ###############

    # Second website to be scraped
    url2 = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
        # This must be re-run every time unless the code is changed to each individual website
    html = browser.html
    soup = bs(html, 'html.parser')
    # Assign the image url for the current featured Mars image
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://jpl.nasa.gov"+image
    # Add to dictionary
    mars_library["featured_image_url"] = featured_image_url

    ############### Mars Weather ###############

    # Third website to be scraped 
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
        # Repost
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    # Add to dictionary
    mars_library["mars_weather"] = mars_weather    
    
    ############### Mars Facts ###############

    # Fourth, but using Pandas
    url4 = "https://space-facts.com/mars/"
    table = pd.read_html(url4)
    # Cleaning of the table
    mars_table = table[0]
    mars_table = mars_table.drop(columns="Earth").rename(columns= {"Mars - Earth Comparison":"","Mars":"Mars Data"}).set_index("")
    html_table = mars_table.to_html()
    html_table = html_table.replace('\n', '')
    html_table
    # Add to dictionary
    mars_library["mars_table"] = html_table

    ############### Mars Hemispheres ###############

    # Fifth
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    hemisphere_image_urls = []
    # Loop through the photos
    for i in range (4):
        images = browser.find_by_tag('h3')
        images[i].click()
            # Required each loop
        html = browser.html
        soup = bs(html, 'html.parser')
        partial_url = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial_url
        dictionary={"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()
    # Add to dictionary
    mars_library["mars_hemisphere"] = hemisphere_image_urls

    # Return Library
    return mars_library
