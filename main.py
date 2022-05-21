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
    def __init__(self, buyprice, curprice, portfolio, stock):
        self.buyprice = buyprice
        self.curprice = curprice
        self.portfolio = portfolio
        self.stock = stock

    def open(self):
        if self.portfolio > 0:
            self.buyprice = self.curprice
            self.stock = self.portfolio / self.buyprice
            self.portfolio = 0
            return self.buyprice, self.stock, self.portfolio
        else:
            pass

    def shortsell(self):
        if self.portfolio == 0:
            self.portfolio = (self.buyprice / self.curprice) * (self.stock * self.buyprice)
            self.stock = 0
            self.buyprice = 0
            return self.buyprice, self.stock, self.portfolio
        else:
            pass

    def longsell(self):
        if self.portfolio == 0:
            self.portfolio = (self.curprice / self.buyprice) * (self.stock * self.buyprice)
            self.buyprice = 0
            self.stock = 0
            return self.buyprice, self.stock, self.portfolio
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
        print(buyorsell)
        print(l3)
        print(pricelist)
        for count, (x, y, z) in enumerate(zip(dif, l3, pricelist)):
            if x > 0 and dif[count - 1] < 0 and z > y:
                buyorsell.append(0)
            elif x < 0 and dif[count - 1] > 0 and dif[count - 2] > 0 and z > y:
                buyorsell.append(1)
            elif x < 0 and dif[count - 1] > 0 and dif[count - 2] > 0 and z < y:
                buyorsell.append(1)
            elif x > 0 and dif[count - 1] < 0 and dif[count - 2] < 0 and dif[count - 3] < 0 and z < y:
                buyorsell.append(0)
            else:
                buyorsell.append(2)

        #print(buyorsell)

        portfoliohistory = []
        print(dif)
        print(buyorsell)
        print(len(buyorsell))
        z = 0
        last = 0
        for i in range(1):
            x = buyorsell[-1]
            y = pricelist[-1]

            action = actions(buyprice, pricelist[-1], portfolio, stock)
            openpos = actions.open(action)
            buyprice = openpos[0]
            stock = openpos[1]
            portfolio = openpos[2]
            print(actions.shortsell(action))

            z += 1

            if portfolio > 0:
                portfoliohistory.append(portfolio)
                last = portfolio
            elif portfolio == 0:
                if shortstock > 0:
                    portvalue = shortstock * (buyprice * (buyprice / y))
                    portfoliohistory.append(portvalue)
                else:
                    portvalue = stock * y
                    portfoliohistory.append(portvalue)
            print("day", z)
            print("actie", x)
            print("hoeveel stocks", stock)
            print("hoeveelheid shortstocks", shortstock)
            print("portfolio doeks", portfoliohistory)

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


