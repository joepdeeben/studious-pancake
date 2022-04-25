import pandas as pd
import requests


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

def

tesla = (datagetter('https://finance.yahoo.com/quote/TSLA/history?p=TSLA'))

tesla =  tesla.values.tolist()
print(tesla)