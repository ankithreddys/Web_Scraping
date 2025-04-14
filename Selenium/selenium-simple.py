from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd


website = "https://www.adamchoi.co.uk/overs/detailed"

driver = webdriver.Chrome()
driver.get(website)
all_matches_button = driver.find_element(By.XPATH,'//label[@analytics-event="All matches"]')
all_matches_button.click()

country_dropdown = Select(driver.find_element(By.ID,"country"))
country_dropdown.select_by_visible_text("USA")

time.sleep(10)

rows = driver.find_elements(By.TAG_NAME,"tr")

date = []
home_team = []
scores = []
away_team = []
for row in rows:
    columns = row.find_elements(By.TAG_NAME,'td')
    if len(columns) == 6:
        date.append(columns[0].text)
        home_team.append(columns[2].text)
        scores.append(columns[3].text)
        away_team.append(columns[4].text)
driver.quit()
data = {"date" : date,
        "home_team": home_team,
        "scores":scores,
        "away_team":away_team}

df = pd.DataFrame(data=data)
df.to_csv("USA_data.csv", index=False)