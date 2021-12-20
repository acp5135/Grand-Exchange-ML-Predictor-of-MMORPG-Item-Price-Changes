import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date

url = "https://secure.runescape.com/m=itemdb_rs/catalogue?cat=1"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
df = pd.DataFrame(columns=['Item', 'Price', 'Change', 'Date'])


def get_string_from_column(columns, columnIndex):
    return columns[columnIndex].text.strip()


for row in soup.select("div table tbody tr"):
    columns = row.findAll("td")

    df = df.append({'Item': get_string_from_column(columns, 0), 'Price': get_string_from_column(columns, 2), 'Change': get_string_from_column(
    columns, 3), 'Date': date.today()}, ignore_index=True)

print(df)