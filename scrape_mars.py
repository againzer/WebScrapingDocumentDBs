from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    #scrape https://redplanetscience.com/ for title and paragraph
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #url of the page to be scraped
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html

    #create bs object parse with parser
    soup = bs(html,'html.parser')

    #scrape title
    title = soup.find(class_= 'content_title')
    news_title = title.text


    #scrape teaser
    paragraph = soup.find(class_= 'article_teaser_body')
    news_p = paragraph.text

    browser.quit()

    #scrape https://spaceimages-mars.com/ for featured image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #url of the page to be scraped
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    html = browser.html

    #create bs object parse with parser
    soup = bs(html,'html.parser')

    #scrape pic
    pic = soup.find(class_= 'headerimage fade-in')
    featured_image_url = str(url+pic['src'])

    browser.quit()

    #scrape https://galaxyfacts-mars.com/ for table
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #url of the page to be scraped
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)

    html = browser.html


    #create bs object parse with parser
    soup = bs(html,'lxml')

    table_html = soup.find(class_="table table-striped")

    table_str = str(table_html)
    table_str

    #code to convert to df not asked to do
    #mars_df = pd.read_html(str(table_html))[0]
    #mars_df

    browser.quit()

    #scrape https://marshemispheres.com/ for table
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    hemisphere_image_urls = []

    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html

    soup = bs(html,'html.parser')

    hemisphere_names = []

    hemisphere_names = soup.find_all('h3')


    for x in range(0,4):
        
        hemisphere_name = hemisphere_names[x].text

        browser.links.find_by_partial_text(hemisphere_name).click()

        html = browser.html

        soup = bs(html,'html.parser')

        pic = browser.links.find_by_text('Sample')['href']

        cerberus_dict = {"title": hemisphere_name ,"img_url": pic}

        hemisphere_image_urls.append(dict(cerberus_dict))

        browser.links.find_by_partial_text('Back').click()
        
    browser.quit()

    #combine everthing to one dictionary
    combined_dictionary = {}
    combined_dictionary["news_title"] = news_title
    combined_dictionary["news_paragraph"] = news_p
    combined_dictionary["featured_image"] = featured_image_url
    combined_dictionary["table_str"] = table_str
    combined_dictionary["image_urls"] = hemisphere_image_urls

    return combined_dictionary