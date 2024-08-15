import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from io import StringIO

headers = {
    'accept-language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

url = 'http://www.nasdaqomxnordic.com/shares/listed-companies/nordic-large-cap'

r = requests.get(url, headers=headers)
table = bs(r.text, 'html.parser').select_one('table#listedCompanies')
df = pd.read_html(StringIO(str(table)))[0]

df.to_csv('nordic_large_cap_companies.csv', index=False)
print("DataFrame saved to nordic_large_cap_companies.csv")
