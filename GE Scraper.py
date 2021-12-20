import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://secure.runescape.com/m=itemdb_rs/catalogue?cat=1"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')
df = pd.DataFrame(columns=['Item', 'Min', 'Max', 'Median', 'Total'])


def get_string_from_column(columns, columnIndex):
    return columns[columnIndex].text.strip()


for row in soup.select("div table tbody tr"):
    columns = row.findAll("td")

    df = df.append({'Item': get_string_from_column(columns, 0), 'Min': get_string_from_column(columns, 2), 'Max': get_string_from_column(
    columns, 3), 'Median': get_string_from_column(columns, 4), 'Total': get_string_from_column(columns, 5)}, ignore_index=True)

print(df)