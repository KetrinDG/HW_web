import lxml
import requests
from bs4 import BeautifulSoup
import os
import json

start_url = "https://quotes.toscrape.com"


def parser_lxml():
    page = ""
    quotes = []
    authors = []
    while True:
        url = f"{start_url}{page}"
        try:
            html = requests.get(url)
        except Exception as e:
            print(f"\033[035mName or service {url} not known\033[0m")
        else:
            if html.status_code != 200:
                print(html)
                break
            soup = BeautifulSoup(html.text, "lxml")
            blocks = soup.find_all("div", class_="quote")
            for block in blocks:
                text = block.find("span", class_="text").text
                author = block.find("small", class_="author").text
                author_url = block.find("a")["href"]
                tags = [el.text for el in block.find_all("a", class_="tag")]
                quotes.append({"quote": text, "author": author, "tags": tags})
                if author not in [el["fullname"] for el in authors]:
                    response = requests.get(f"{start_url}{author_url}")
                    soup_author = BeautifulSoup(response.text, "lxml")
                    born_date = soup_author.find("span", class_="author-born-date").text
                    born_location = soup_author.find(
                        "span", class_="author-born-location"
                    ).text
                    description = soup_author.find(
                        "div", class_="author-description"
                    ).text
                    authors.append(
                        {
                            "fullname": author,
                            "born_date": born_date,
                            "born_location": born_location,
                            "description": description,
                        }
                    )
            try:
                page = soup.find("li", attrs={"class": "next"}).find("a")["href"]
            except AttributeError:
                print("End")
                break

    if quotes:
        with open(os.path.join("data", "qoutes.json"), "w") as f:
            json.dump(quotes, f)

    if authors:
        with open(os.path.join("data", "authors.json"), "w") as f:
            json.dump(authors, f)
