import requests
from bs4 import BeautifulSoup as bsp
import re

root = "https://subslikescript.com"
website = f"{root}/movies"
result = requests.get(website)
content = result.text

soup = bsp(content, "lxml")
box = soup.find("article", class_="main-article")

movie_list = box.find_all("a", href=True)

for link in movie_list:
    title = link.get_text(strip=True)
    href = link["href"]

    movie_url = f"{root}/{href}"
    website_result = requests.get(movie_url)
    website_soup = bsp(website_result.text, "lxml")
    website_box = website_soup.find("article", class_="main-article")

    try:
        movie_title = website_box.find('h1').get_text()
        transcript = website_box.find("div", class_="full-script").get_text(strip=True, separator=" ")
    except AttributeError:
        print(f"Could not fetch script for {title}")
        continue

    safe_title = re.sub(r'[\\/*?:"<>|]', "", movie_title)

    with open(f"{safe_title}.txt", "w", encoding="utf-8") as file:
        file.write(transcript)

    print(f"Saved: {safe_title}")
