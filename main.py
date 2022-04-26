import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

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
ema = 0
ema2 = 0

l = []
l2 = []
tsma = tesla[0:12]
tsma2 = tesla[0:26]

for count, x in enumerate(tsma):
        str1 = ''.join(x)
        str1 = float(str1)
        str2 = ''.join(tsma[count-1])
        str2 = float(str2)
        ema = (str1 * 0.15384615384) + (str2 * (1 - 0.15384615384))
        l.append(ema)
for count, x in enumerate(tsma2):
        str1 = ''.join(x)
        str1 = float(str1)
        str2 = ''.join(tsma2[count-1])
        str2 = float(str2)
        ema = (str1 * 0.07407407407) + (str2 * (1 - 0.07407407407))
        l2.append(ema)

macd = []
for x, y in zip(l,l2):
        macd.append(x-y)
print(macd)
print(l)
plt.plot(l2)
plt.plot(l)
plt.show()
