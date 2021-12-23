import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
from pymongo import MongoClient
import pymongo
import dns
import os

mongo_pwd = os.environ['MDB_pwd']

url = "https://secure.runescape.com/m=itemdb_rs/catalogue?cat=1"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
df = pd.DataFrame(columns=['Item', 'Price', 'Change', 'Date'])


def get_string_from_column(columns, columnIndex):
    return columns[columnIndex].text.strip()


for row in soup.select("div table tbody tr"):
    columns = row.findAll("td")

    df = df.append({'Item': get_string_from_column(columns, 0), 'Price': get_string_from_column(columns, 2), 'Change': get_string_from_column(
    columns, 3), 'Date': str(date.today())}, ignore_index=True)

cluster = MongoClient(f"mongodb+srv://acp5135:{mongo_pwd}@cluster0.2sduf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["RS_Data"]
collection = db["Daily_items"]

df.reset_index(inplace=True)

print(df)
post = df.to_dict("records")
collection.insert_many(post)
