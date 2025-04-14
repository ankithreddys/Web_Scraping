from selenium import webdriver
import time 
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options

options = Options()
#options.add_argument("--headless")
#options.add_argument("--window-size=1920,1080")


website = "https://www.audible.com/search"
driver = webdriver.Chrome(options=options)
driver.get(website)
driver.maximize_window()

pagination = driver.find_element(By.XPATH, "//div[@class='linkListWrapper']")
pages = pagination.find_elements(By.TAG_NAME,"li")
last_page = int(pages[-2].text)

book_name = []
author_name = []
duration = []

for page in range(last_page):
    page_container = driver.find_element(By.CLASS_NAME,"adbl-impression-container")
    products = page_container.find_elements(By.XPATH,'.//li[contains(@class,"productListItem")]')

    for product in products:
        book = product.find_element(By.XPATH,'.//h3[contains(@class,"bc-heading")]').text
        author = product.find_element(By.XPATH,'.//li[contains(@class,"authorLabel")]').text
        length = product.find_element(By.XPATH,'.//li[contains(@class,"runtimeLabel")]').text
        book_name.append(book)
        author_name.append(author)
        duration.append(length)
    next_page = driver.find_element(By.XPATH,"//span[contains(@class,'nextButton')]")
    next_page.click()
driver.quit()

df = pd.DataFrame({'Book_name':book_name, 'Author_name' : author_name, 'Duration' : duration})
df.to_csv("Audible_data.csv",index=False)
