from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
browser = webdriver.Chrome("chromedriver.exe") #webdriver.nameOfTheBrowser("path of the webdriver.exe file")
browser.get(START_URL) #Open the link 

time.sleep(10)

planets_data = []

def scrape():

    for i in range(0,10):
        print(f'Scrapping page {i+1} ...' )
        
        # BeautifulSoup Object     
        soup = BeautifulSoup(browser.page_source, "html.parser")
        
        current_page_number = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
        if current_page_number<i:
            browser.find_element(by = By.XPATH, value = '//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
        elif current_page_number>i:
            browser.find_element(by = By.XPATH, value = '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        else:
            break

        # Loop to find element using XPATH
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):

            li_tags = ul_tag.find_all("li")
           
            temp_list = []

            for index, li_tag in enumerate(li_tags):

                if index == 0:                   
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            
            #get the hyperlink tag ---> <a href=""></a>
            hyperlink = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink.find_all("a",href=True)[0]["href"])
            
            planets_data.append(temp_list)

        # Find all elements on the page and click to move to the next page
        browser.find_element(by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

# Calling Method    
scrape()

# Define Header
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink"]

# Define pandas DataFrame   
planet_df_1 = pd.DataFrame(planets_data, columns=headers)

# Convert to CSV
planet_df_1.to_csv('c128PartialOutput.csv',index=True, index_label="id")


    

