import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import time

n = []
print('how many tickers?')
portfolio = 1000
buyprice = 0
stock = 0
pos = 2
class calcs:
    def __init__(self, pricelist, period):
        self.pricelist = pricelist
        self.k = (2 / period+1)
        self.emalist = [self.pricelist[0]]

    def ema(self):
        for count, x in enumerate(self.pricelist):
            str1 = x
            str2 = self.emalist[count]
            ema1 = (str1 * self.k) + (str2 * (1 - self.k))
            self.emalist.append(ema1)
        return self.emalist

class actions:
    def __init__(self, buyprice, curprice, portfolio, stock, pos):
        self.buyprice = buyprice
        self.curprice = curprice
        self.portfolio = portfolio
        self.stock = stock
        self.pos = pos
    def open(self):
        if self.portfolio > 0:
            self.buyprice = self.curprice
            self.stock = self.portfolio / self.buyprice
            self.portfolio = 0
            self.pos = 0
            return self.buyprice, self.stock, self.portfolio, self.pos
        else:
            pass

    def openshort(self):
        if self.portfolio > 0:
            self.buyprice = self.curprice
            self.stock = self.portfolio / self.buyprice
            self.portfolio = 0
            self.pos = 1
            return self.buyprice, self.stock, self.portfolio, self.pos
        else:
            pass

    def shortsell(self):
        if self.portfolio == 0:
            self.portfolio = (self.buyprice / self.curprice) * (self.stock * self.buyprice)
            self.stock = 0
            self.buyprice = 0
            self.pos = 2
            return self.buyprice, self.stock, self.portfolio, self.pos
        else:
            pass

    def longsell(self):
        if self.portfolio == 0:
            self.portfolio = (self.curprice / self.buyprice) * (self.stock * self.buyprice)
            self.buyprice = 0
            self.stock = 0
            self.pos = 2
            return self.buyprice, self.stock, self.portfolio, self.pos
        else:
            pass


tickerscount = int(input())
for x in range(tickerscount):
    print('enter ticker')
    tick = input()
    tick = tick.upper()
    n.append(tick)
print("timeframe in seconds")
timeframe = int(input())
for x in n:
    def datagetter(link):
        r = requests.get(link, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        data = pd.read_html(r.text)
        data = data[0]
        close = data[['Close*']]
        return close


    link = 'https://finance.yahoo.com/quote/TSLA/history?p=TSLA'
    link = link.replace("TSLA", x)


    tesla = []
    price = []
    for x in range(26):
        price = (datagetter(link))
        price = price.values.tolist()
        tesla.append(price[0])
        time.sleep(timeframe)
        print(x + 1, tesla)
    looper = 1


    while looper < 2:
        time.sleep(timeframe)
        price = (datagetter(link))
        price = price.values.tolist()
        del tesla[0]
        tesla.append(price[0])
        print(tesla)


        pricelist = []


        for count, x in enumerate(tesla):
            str1 = ''.join(x)
            try:
              str1 = float(str1)
              pricelist.append(str1)
            except ValueError:
               pass
        print(len(pricelist))
        pricelist = pricelist[0:26]
        pricelist = pricelist[::-1]



        # calculates the 12 period ema
        list1 = calcs(pricelist, 12)
        l = list1.ema()
        print(l)

        #calculates the 26 period ema
        list2 = calcs(pricelist, 26)
        l2 = list2.ema()
        print(l2)

        #calulates 200 period ema
        list3 = calcs(pricelist, 50)
        l3 = list3.ema()
        print(l3)

        macd = []
        for x, y in zip(l, l2):
            macd.append(x - y)




        #print(macd)
        signalline = [macd[0]]

        for count, x in enumerate(macd):
            str4 = signalline[count]
            ema2 = (x * 0.2) + (str4 * (1 - 0.2))
            signalline.append(ema2)


        signalline = signalline[1:]
        #print(signalline)
        dif = []
        for x, y in zip(macd, signalline):
            verschil = x - y
            dif.append(verschil)

        #print(dif)

        buyorsell = []
        print(l3)
        print(pricelist)
        action = actions(buyprice, pricelist[-1], portfolio, stock, pos)
        print(dif)
        print(buyprice, pricelist[-1], portfolio, stock, pos)
        if dif[-2] > 0 and dif[-1] < 0 and pricelist[-1] > l3[-1] and pos == 2:
            openpos = actions.open(action)
            buyprice = openpos[0]
            stock = openpos[1]
            portfolio = openpos[2]
            pos = openpos[3]
        elif dif[-2] < 0 and dif[-1] > 0 and pricelist[-1] < l3[-1] and pos == 2:
            openpos = actions.openshort(action)
            buyprice = openpos[0]
            stock = openpos[1]
            portfolio = openpos[2]
            pos = openpos[3]
        elif pos == 0 and (pricelist[-1] / buyprice > 1.01 or pricelist[-1] / buyprice > 0.99):
            closelong = actions.longsell(action)
            buyprice = closelong[0]
            stock = closelong[1]
            portfolio = closelong[2]
            pos = closelong[3]
        elif pos == 1 and (buyprice / pricelist[-1] < 1.01 or buyprice / pricelist[-1] > 0.99):
            closeshort = actions.shortsell(action)
            buyprice = closeshort[0]
            stock = closeshort[1]
            portfolio = closeshort[2]
            pos = closeshort[3]
        else:
            pass

        print(buyprice, pricelist[-1], portfolio, stock, pos)


        print(portfolio)


        #x2 = np.array([i for i in range(len(portfoliohistory))])

        profit = []

        #for x in portfoliohistory:
            #profit.append(x)

        #print(portfoliohistory)
        # X_Y_Spline2 = make_interp_spline(x2, portfoliohistory)
        #
        # X_2 = np.linspace(x2.min(), x2.max(), 50)
        # Y_2 = X_Y_Spline2(X_2)
        #
        # X_Y_Spline3 = make_interp_spline(x2, profit)
        #
        # Y_3 = X_Y_Spline3(X_2)
        #
        # plt.plot(X_2, Y_2)
        # plt.plot(X_2, Y_3)
        # plt.legend(n)
        # plt.show()


