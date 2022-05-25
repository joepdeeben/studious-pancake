import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import time, random

n = []
portfolio = 1000
buyprice = 0
stock = 0
pos = 2
portfoliohistory = []
class calcs:
    def __init__(self, pricelist, period):
        self.pricelist = pricelist
        self.k = (2 / (period+1))
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

user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


print('take profit at what percentage?')
takeprofitpercent = float(input())
takeprofitpercent = takeprofitpercent / 100
takeprofit = 1 + takeprofitpercent
takeloss = 1 - takeprofitpercent
print(takeprofit, takeloss)
print('how many tickers?')
tickerscount = int(input())
for x in range(tickerscount):
    print('enter ticker')
    tick = input()
    tick = tick.upper()
print("timeframe in seconds")
timeframe = int(input())
def datagetter(link):
    try:
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        r = requests.get(link, headers=headers)
        data = pd.read_html(r.text)
        data = data[0]
        close = data[['Close*']]
        return close
    except ConnectionResetError or ChunkedEncodingError:
        return pricelist[-1]


link = 'https://finance.yahoo.com/quote/TSLA/history?p=TSLA'
link = link.replace("TSLA", tick)


tesla = []
price = []
for x in range(200):
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


    pricelist = []


    for count, x in enumerate(tesla):
        str1 = ''.join(x)
        try:
          str1 = float(str1)
          pricelist.append(str1)
        except ValueError:
           pass
    print(pricelist)
    pricelist = pricelist[0:200]



    # calculates the 12 period ema
    list1 = calcs(pricelist, 12)
    l = list1.ema()
    print(l)

    #calculates the 26 period ema
    list2 = calcs(pricelist, 26)
    l2 = list2.ema()
    print(l2)

    #calulates 50 period ema
    list3 = calcs(pricelist, 200)
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


    #print(signalline)
    dif = []
    for x, y in zip(macd, signalline):
        verschil = x - y
        dif.append(verschil)

    #print(dif)

    action = actions(buyprice, pricelist[-1], portfolio, stock, pos)
    print(dif[-2], dif[-1])
    print(l3[-1])
    print(buyprice, pricelist[-1], portfolio, stock, pos)
    if dif[-2] < 0 and dif[-1] > 0 and pricelist[-1] > l3[-1] and pos == 2:
        openpos = actions.open(action)
        buyprice = openpos[0]
        stock = openpos[1]
        portfolio = openpos[2]
        pos = openpos[3]
    elif dif[-2] > 0 and dif[-1] < 0 and pricelist[-1] < l3[-1] and pos == 2:
        openshort = actions.openshort(action)
        buyprice = openshort[0]
        stock = openshort[1]
        portfolio = openshort[2]
        pos = openshort[3]
    elif pos == 0 and (pricelist[-1] / buyprice > takeprofit or pricelist[-1] / buyprice < takeloss):
        closelong = actions.longsell(action)
        buyprice = closelong[0]
        stock = closelong[1]
        portfolio = closelong[2]
        pos = closelong[3]
    elif pos == 1 and (buyprice / pricelist[-1] > takeprofit or buyprice / pricelist[-1] < takeloss):
        closeshort = actions.shortsell(action)
        buyprice = closeshort[0]
        stock = closeshort[1]
        portfolio = closeshort[2]
        pos = closeshort[3]
    else:
        pass




    print(buyprice, pricelist[-1], portfolio, stock, pos)
    if stock > 0:
        if pos == 1:
            print(buyprice / pricelist[-1])
            print((buyprice / pricelist[-1]) * stock)
        elif pos == 0:
            print(pricelist[-1] / buyprice)
            print((pricelist[-1] / buyprice) * stock)
    else:
       print(portfolio)
       portfoliohistory.append(portfolio)
    print(portfoliohistory)


    # if len(portfoliohistory) > 4:
    #     x2 = np.array([i for i in range(len(portfoliohistory))])
    #
    #     profit = []
    #
    #     for x in portfoliohistory:
    #         profit.append(x)
    #
    #     print(portfoliohistory)
    #     X_Y_Spline2 = make_interp_spline(x2, portfoliohistory)
    #
    #     X_2 = np.linspace(x2.min(), x2.max(), 50)
    #     Y_2 = X_Y_Spline2(X_2)
    #
    #     X_Y_Spline3 = make_interp_spline(x2, profit)
    #
    #     Y_3 = X_Y_Spline3(X_2)
    #
    #     plt.plot(X_2, Y_2)
    #     plt.plot(X_2, Y_3)
    #     plt.legend(n)
    #     plt.show()
    #     plt.close()
    # else:
    #     pass


