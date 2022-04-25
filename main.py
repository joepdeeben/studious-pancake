import pandas as pd
import requests
import numpy as np

name = requests.get('https://finance.yahoo.com/trending-tickers' ,headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
data1 = pd.read_html(name.text)
data1 = data1[0]
names = data1[['Symbol']]


def datagetter(link):
        r = requests.get(link ,headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        data = pd.read_html(r.text)
        data = data[0]
        close = data[['Close*']]
        return close

tesla = (datagetter('https://finance.yahoo.com/quote/TSLA/history?p=TSLA'))

tesla = tesla.values.tolist()
del tesla[-1]
print(tesla)
sma = 0
for x in tesla[0:12]:
        str1 = ''.join(x)
        str1 = float(str1)
        sma += str1


sma = sma / 12
print(sma)

