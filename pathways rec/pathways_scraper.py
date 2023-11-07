import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def exist():
    driver = webdriver.Safari()
    modules_dict = {}
    num = 1
    while True:
        tail = "?page=" + str(num)
        url = "https://pathways.duke.edu/searchPage" + tail
        response = requests.get(url)
        if response.status_code == 200:
            driver.get(url)
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/main/div[4]/div[1]/div[1]/div/div[2]')))                                                                            
                text = element.text
                if len(text) > 0:
                    titles = []
                    descriptions = []
                    for i in range(1, 6):
                        try:
                            title_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/main/div[4]/div[' + str(i) + ']/div[1]/div/div[2]')))
                            title = title_search.text
                            description_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/main/div[4]/div[' + str(i) + ']/div[1]/div/div[3]')))                                                                                     
                            description = description_search.text
                            titles.append(title)
                            descriptions.append(description)
                        except Exception as e:
                            print("Error: Could not find a", i, "th element on page", num)
                    modules_dict[num] = {'titles': titles, 'descriptions': descriptions}
                else:
                    print("No data on page", "\nThe page number is:", num)
            except Exception as e:
                print("Error: There are no modules on the", num, "th page")
                break
            num += 1 
    driver.quit()
    return modules_dict

def write(data):
    with open('data/all_modules.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Page Number', 'Title', 'Description'])
        for page_num, page_data in data.items():
            titles = page_data['titles']
            descriptions = page_data['descriptions']
            for title, description in zip(titles, descriptions):
                csvwriter.writerow([page_num, title, description])

write(exist())

data = exist()
