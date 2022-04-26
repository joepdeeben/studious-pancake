import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

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

for x in enumerate(tesla):
        print(x)

ema = 0
ema2 = 0

l = []
l2 = []

tsma = tesla[0:61]
tsma2 = tesla[0:61]

tsma = tsma[::-1]
tsma2 = tsma2[::-1]

#calculates the 12 period ema
for count, x in enumerate(tsma):
        str1 = ''.join(x)
        str1 = float(str1)
        str2 = ''.join(tsma[count-1])
        str2 = float(str2)
        ema1 = (str1 * 0.15384615384) + (str2 * (1 - 0.15384615384))
        l.append(ema1)

#calculates the 26 period ema
for count, x in enumerate(tsma2):
        str1 = ''.join(x)
        str1 = float(str1)
        str2 = ''.join(tsma2[count-1])
        str2 = float(str2)
        ema2 = (str1 * 0.07407407407) + (str2 * (1 - 0.07407407407))
        l2.append(ema2)

l = l[::-1]
l2 = l2[::-1]

print(l)
print(l2)

macd = []
for x, y in zip(l,l2):
        macd.append(x-y)

macd = macd[0:61]
macd = macd[::-1]

print(macd)

signalline = []

for count, x in enumerate(macd):
        str4 = macd[count-1]
        ema2 = (x * 0.2) + (str4 * (1 - 0.2))
        signalline.append(ema2)

print(signalline)

x = np.array([i for i in range(61)])

X_Y_Spline1 = make_interp_spline(x, macd)

X_1 = np.linspace(x.min(), x.max(), 50)
Y_1 = X_Y_Spline1(X_1)

plt.plot(X_1, Y_1)

X_Y_Spline = make_interp_spline(x, signalline)

X_ = np.linspace(x.min(), x.max(), 50)
Y_ = X_Y_Spline(X_)

plt.plot(X_, Y_)
plt.show()
