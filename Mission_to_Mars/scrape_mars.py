from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd


def scrape():
    #scrape (https://redplanetscience.com/)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup (html, "html.parser")

    news_title=soup.find("div", class_="content_title").get_text()
    news_p=soup.find("div", class_="article_teaser_body").get_text()

    browser.quit()

    #scrape (https://spaceimages-mars.com)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://spaceimages-mars.com"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup (html, "html.parser")

    temp_url = soup.find("a", class_="showimg fancybox-thumbs")
    featured_image_url = "https://spaceimages-mars.com/" + temp_url["href"]

    browser.quit()

    #scrape (https://galaxyfacts-mars.com)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://galaxyfacts-mars.com"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup (html, "html.parser")

    tables = pd.read_html(url)
    tables

    mars_df=tables[1]
    mars_df.columns = ["Facts", "Values"]
    mars_df

    mars_html_table = mars_df.to_html(index=False)
    mars_html_table

    mars_html_table.replace('\n', '')

    #scrape (https://marshemispheres.com/)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup (html, "html.parser")

    hemisphere_dict=[]

    hemisphere_list = soup.findAll("div", class_="description")

    for i in range(4):

        hemisphere = hemisphere_list[i]
        temp_url=hemisphere.find("a")
        hemisphere_page_url = "https://marshemispheres.com/" + temp_url["href"]
        hempishere_title = hemisphere.find("h3").get_text()


        url = hemisphere_page_url
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup (html, "html.parser")

        hemisphere_image_find = soup.find("img", class_= "wide-image")
        hemisphere_image_url = "https://marshemispheres.com/" + hemisphere_image_find["src"]
    
        hemisphere_dict.append({"title": hempishere_title, "imageurl": hemisphere_image_url})

        mars_data = { "mars_news_title": news_title,
                  "mars_news_paragraph": news_p,
                  "mars_image1": featured_image_url,
                  "mars_facts_html": mars_html_table,
                  "mars_hemisphere_images":  hemisphere_dict}

    return mars_data