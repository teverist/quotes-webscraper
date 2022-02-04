import requests
import bs4
from bs4 import BeautifulSoup
import urllib.request
import time
import pandas
from pandas import DataFrame
from sqlalchemy import create_engine


url = "http://quotes.toscrape.com/page/"
quote_author = []
quote_text = []



def scraping(webpage, page_number):
    next_page = webpage + str(page_number)
    response = requests.get(str(next_page))
    soup = BeautifulSoup(response.text, "html.parser")
    soup_quote = soup.findAll("span", {"class": "text"})
    soup_author = soup.findAll("small", {"class": "author"})

    for x in range(len(soup_author)):
        quote_author.append(soup_author[x].text)
        quote_text.append(soup_quote[x].text)

    if page_number < 10:
        page_number = page_number + 1
        scraping(url, page_number)


def addToDB(dataframe):
    engine = create_engine('sqlite://', echo=False)
    dataframe.to_sql('quotes', con=engine)

    print(engine.execute("SELECT * FROM quotes").fetchall())

if __name__ == "__main__":
    scraping(url, 1)

    data = {'Quote_Author': quote_author, 'Quote_Text': quote_text}

    df = DataFrame(data, columns=['Quote_Author', 'Quote_Text'])

    addToDB(df)



