from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import csv
from bs4 import BeautifulSoup
import re
import time

# NYT

#Pseudocode:
#NYT
#to be run on the same day (if need be, take a snapshot from the wayback machine)
#Within a class, initialize the webdriver
#Function to scrape links to the four subtopics of interest: "US, World, Science, Health"
#Within subtopic pages, scrape all links and link titles and associated image if present
#scrolling might be an issue
#visit all links
#need to store each tag in the corner of the screen, along with all alt text for each image
#write to csv with 
#how to go from link to image to download image 


#functions:
'''
Function for main scrape
function for getting element
function for getting url
function for getting image
function for turning image into array
function for writing to csv
'''

class Web_Scrape_NYT:
    def __init__(self):
        # Initialize the webdriver
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        self.front_page = {}

    def get_front_page_links(self):
        self.driver.get("https://www.nytimes.com")

        pages_of_interest = ["World", "U.S.", "Health", "Science"]
        TopPage = self.driver.find_elements(By.CLASS_NAME, "css-1wjnrbv")
        TopPage_Text = [Top.get_attribute("text") for Top in TopPage]
        TopPage_HREF = [Top.get_attribute("href") for Top in TopPage]
        for i in range(len(TopPage_Text)):
            if TopPage_Text[i] in pages_of_interest:
                self.front_page[TopPage_Text[i]] = TopPage_HREF[i]
        #self.driver.close()
        return self.front_page
    
    def get_titles_links(self):
        href_elements = self.driver.find_elements(By.XPATH, "//div[@class='css-1l4spti']/a")
        list_of_hrefs = [href.get_attribute('href') for href in href_elements]
        
        title_elements = self.driver.find_elements(By.XPATH, "//div[@class='css-1l4spti']//h2[@class='css-1kv6qi e15t083i0']")
        #i used title.text instead of get_attribute('text') because I think we don't actually have a text attribute here
        list_of_titles = [title.text for title in title_elements]
        return list_of_hrefs, list_of_titles

    def get_images(self):
        picture_elements = self.driver.find_elements(By.XPATH, "//section[@id='stream-panel']//img[@alt and @class='css-rq4mmj']")
        #i used title.text instead of get_attribute('text') because I think we don't actually have a text attribute here
        list_of_pics = [pic.get_attribute('src') for pic in picture_elements]
        j=0
        for i in list_of_pics:
            self.driver.get(i)
            self.driver.save_screenshot(str(i)+".png")
            j = j+1

        print(len(list_of_pics))

    def scroll_to_bottom_of_page(self, url):
        print("starting new scroll")
        self.driver.get(str(url))
        time.sleep(1)
        i = 1
        k = 20
        for i in range(30):
            last_height = self.driver.execute_script('return document.body.scrollHeight')
            print("scrolling")
            howmany = self.driver.find_elements(By.CLASS_NAME, "css-112uytv")
            #print(len(howmany))
            increment = int(int(last_height)/30)
            time.sleep(.5)
            if k == 20:
                k = 30
            elif k == 30:
                k = 20
            for i in range(k):
                self.driver.execute_script('window.scrollTo(0,' + str(increment*i)+')')
                i = i+1
                time.sleep(.2)    
        WSNYT.get_images()
        list_of_hrefs, list_of_titles = WSNYT.get_titles_links()
        print(list_of_hrefs, list_of_titles)
        return list_of_hrefs, list_of_titles

    def get_articles(self):
        Front_Page = self.get_front_page_links()
        print(Front_Page.values())


WSNYT = Web_Scrape_NYT()
#WSNYT.scroll_to_bottom_of_page("https://www.nytimes.com/international/section/world")
hrefs_titles_dicts = []
list_of_pages = WSNYT.get_front_page_links()
print(list_of_pages)


import pandas as pd
for key, section in list_of_pages.items():
    list_of_hrefs, list_of_titles = WSNYT.scroll_to_bottom_of_page(section)

    for i in range(len(list_of_hrefs)):
        hrefs_titles_dicts.append({"Title": str(list_of_titles[i]), "Link": str(list_of_hrefs[i])})
    df = pd.DataFrame(hrefs_titles_dicts)
    df.to_csv(str(key)+'.csv', index=False, header=True)
    




