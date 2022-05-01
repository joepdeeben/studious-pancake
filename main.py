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
print("which ticker")
ticker = input()
ticker = ticker.upper()

link = 'https://finance.yahoo.com/quote/TSLA/history?p=TSLA'
link = link.replace("TSLA", ticker )

tesla = (datagetter(link))

tesla = tesla.values.tolist()
del tesla[-1]

pricelist = []

for count, x in enumerate(tesla):
        str1 = ''.join(x)
        str1 = float(str1)
        pricelist.append(str1)

ema = 0
ema2 = 0

l = []
l2 = []

tsma = tesla[0:93]
tsma2 = tesla[0:93]

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


macd = []
for x, y in zip(l,l2):
        macd.append(x-y)

macd = macd[0:93]
macd = macd[::-1]

print(macd)

signalline = []

for count, x in enumerate(macd):
        str4 = macd[count-1]
        ema2 = (x * 0.2) + (str4 * (1 - 0.2))
        signalline.append(ema2)

print(signalline)


dif = []
for x, y in zip(macd, signalline):
        verschil = x - y
        dif.append(verschil)

print(dif)

buyorsell = []

for count, x in enumerate(dif):
        if x > 0 and dif[count-1] < 0:
                buyorsell.append(1)
        elif x < 0  and dif[count-1] > 0:
                buyorsell.append(0)
        elif x < 0 and dif[count - 1] < 0:
                buyorsell.append(2)
        elif x > 0 and dif[count - 1] > 0:
                buyorsell.append(2)



l = l[::-1]
l2 = l2[::-1]

print(l)
print(l2)

print(buyorsell)
pricelist = pricelist[::-1]

print(pricelist)

portfoliohistory = []

portfolio = 1000
stock = 0
z = 0
last = 0
for x, y in zip(buyorsell, pricelist):
        if x == 2:
                y = y
                portfolio = portfolio
                stock = stock
        elif x == 0:
                stock = portfolio / y
                portfolio = 0
        elif x == 1:
            if stock == 0:
                portfolio = portfolio
            else:
                portfolio = stock * y
                stock = 0
        z += 1

        if portfolio > 0:
                portfoliohistory.append(portfolio)
                last = portfolio
        elif portfolio < 0:
                portfoliohistory.append(portfolio)
        print("day", z)
        print("actie", x)
        print("hoeveel stocks", stock)
        print("portfolio doeks",portfolio)






print(portfoliohistory)


x2 = np.array([i for i in range(len(portfoliohistory))])

profit = []

for x in portfoliohistory:
    profit.append(x - 1000)

print(profit)
X_Y_Spline2 = make_interp_spline(x2, portfoliohistory)

X_2 = np.linspace(x2.min(), x2.max(), 50)
Y_2 = X_Y_Spline2(X_2)

X_Y_Spline3 = make_interp_spline(x2, profit)

Y_3 = X_Y_Spline3(X_2)

plt.plot(X_2, Y_2)
plt.plot(X_2,Y_3)
plt.show()