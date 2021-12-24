import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
from pymongo import MongoClient
import pymongo
import dns
import os

mongo_pwd = os.environ['MDB_pwd']

url2 = "https://secure.runescape.com/m=itemdb_rs/catalogue"
r = requests.get(url2)
soup2 = BeautifulSoup(r.content, 'html.parser')
df = pd.DataFrame(columns=['URL', 'Category'])


for row in soup2.select("div main div li"):
    element = row.find("a")
    url3 = element.get('href')
    text = element.get_text()
    df = df.append({'URL': url3, 'Category': text}, ignore_index=True)

df = df.iloc[4:]

def get_string_from_column(columns, columnIndex):
    return columns[columnIndex].text.strip()

for i in df['URL'].tolist():
    
    url = f"https://secure.runescape.com/m=itemdb_rs/{i}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    df = pd.DataFrame(columns=['Item', 'Price', 'Change', 'Date'])
    
    

    
    
    for row in soup.select("div table tbody tr"):
        columns = row.findAll("td")
    
        df = df.append({'Item': get_string_from_column(columns, 0), 'Price': get_string_from_column(columns, 2),\
        'Change': get_string_from_column(columns, 3), 'Date': str(date.today())}, ignore_index=True)
    
    cluster = MongoClient(f"mongodb+srv://acp5135:{mongo_pwd}@cluster0.2sduf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster["RS_Data"]
    collection = db["Daily_items"]
    
    df.reset_index(inplace=True)
    
    print(df)
    post = df.to_dict("records")
    collection.insert_many(post)
