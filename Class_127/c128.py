from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import time

#NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
browser = webdriver.Chrome("chromedriver.exe") #webdriver.nameOfTheBrowser("path of the webdriver.exe file")
browser.get(START_URL) #Open the link 

time.sleep(10)

new_planets_data = []

def scrape_more(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []
        for tr in soup.find_all("tr", attrs= {"class": "fact_row"}):
            td = tr.find_all("td")
            for i in td:
                try:
                    temp_list.append(i.find_all("div", attrs = {"class", "value"})[0].contents[0])
                except:
                    temp_list.append("")
            
        new_planets_data.append(temp_list)
            
    except:
        time.sleep(1)
        scrape_more(hyperlink)

planet_data = pd.read_csv("c128PartialOutput.csv")

#iterrows()
for index, value in planet_data.iterrows():
    print(value['hyperlink'])
    scrape_more(value['hyperlink'])
    print("Scrapping the data at the hyperlink:", index+1, "...completed")

print(planet_data[0:10])

##replace(value need to be replaced, the new value)

scrapped_data=[]

for row in planet_data:
    new_data = []
    for j in row:
        j = j.replace("\n", "")
        new_data.append(j)
    scrapped_data.append(new_data)
print(scrapped_data)

headers=["Planet_Type", "Discovery_Date", "Mass", "Planet_Radius", "Orbital_Radius", "Orbital_Period", "Eccentricity", "Dectection_Method"]
output = pd.DataFrame(scrapped_data, columns = headers)
output.to_csv("c128Output.csv", index = True, index_label = "id")