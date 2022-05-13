import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

n = []
print('how many tickers?')

tickerscount = int(input())
for x in range(tickerscount):
    print('enter ticker')
    tick = input()
    n.append(tick)

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

    tesla = (datagetter(link))

    tesla = tesla.values.tolist()
    del tesla[-1]

    pricelist = []

    for count, x in enumerate(tesla):
        str1 = ''.join(x)
        try:
          str1 = float(str1)
          pricelist.append(str1)
        except ValueError:
           pass
    ema = 0
    ema2 = 0
    print(len(pricelist))
    pricelist = pricelist[0:93]
    pricelist = pricelist[::-1]
    l = [pricelist[0]]
    l2 = [pricelist[0]]

    #calculate rsi
    counter = 0
    fe = 7
    le = 14

    avgp = []
    avgl = []
    avgloss = 0
    avgprofit = 0


    print(pricelist)


    for count, x in enumerate(pricelist[0:7]):
        if x > pricelist[count - 1]:
            avgprofit += (x / pricelist[count - 1])
        elif x < pricelist[count - 1]:
            avgloss += (pricelist[count - 1] / x)
    avgp.append(avgprofit / 7)
    avgl.append(avgloss / 7)
    avgprofit = 0
    avgloss = 0

    while counter < ((len(pricelist) / 7) - 7):
       for count, x in enumerate(pricelist[fe:le]):
           if x > pricelist[count-1]:
               avgp.append((avgp[-1] * 7 + (((x / pricelist[count-1]) - 1) * 100)) / 7)
               avgl.append(0)
           elif x < pricelist[count-1]:
               avgl.append((avgl[-1] * 7 + (((pricelist[count-1] / x) - 1) * 100)) / 7)
               avgp.append(0)
       counter += 1
       fe += 7
       le += 7
















    gd = pricelist[0] / pricelist[-1]




    # calculates the 12 period ema
    for count, x in enumerate(pricelist):
        str1 = x
        str2 = l[count]
        ema1 = (str1 * 0.15384615384) + (str2 * (1 - 0.15384615384))
        l.append(ema1)

    # calculates the 26 period ema
    for count, x in enumerate(pricelist):
        str1 = x
        str2 = (l2[count])
        ema2 = (str1 * 0.07407407407) + (str2 * (1 - 0.07407407407))
        l2.append(ema2)
    print(l)
    print(l2)

    macd = []
    for x, y in zip(l, l2):
        macd.append(x - y)




    print(macd)
    signalline = [macd[0]]

    for count, x in enumerate(macd):
        str4 = signalline[count]
        ema2 = (x * 0.2) + (str4 * (1 - 0.2))
        signalline.append(ema2)


    signalline = signalline[1:]
    print(signalline)
    dif = []
    for x, y in zip(macd, signalline):
        verschil = x - y
        dif.append(verschil)

    print(dif)

    buyorsell = []

    for count, x in enumerate(dif):
        if x > 0 and dif[count - 1] > 0 and dif[count - 2] < 0:
            buyorsell.append(0)
        elif x < 0 and dif[count - 1] > 0:
            buyorsell.append(1)
        elif x < 0 and dif[count - 1] < 0:
            buyorsell.append(1)
        elif x > 0 and dif[count - 1] > 0:
            buyorsell.append(2)

    print(buyorsell)

    portfoliohistory = []

    portfolio = 1000
    stock = 0
    shortstock = 0
    buyprice = 0
    z = 0
    last = 0
    for x, y in zip(buyorsell, pricelist):
        if x == 2:
            y = y
            portfolio = portfolio
            stock = stock
        elif x == 0:
            if shortstock > 0:
                portfolio = shortstock * (buyprice * (buyprice / y))
                shortstock = 0
                stock = portfolio / y
                portfolio = 0
            elif stock == 0:
                stock = portfolio / y
                portfolio = 0
            else:
                stock = stock
        elif x == 1:
            if stock == 0 and portfolio == 0:
                portfolio = portfolio
            else:
                if portfolio == 0:
                    portfolio = stock * y
                    stock = 0
                    shortstock = portfolio / y
                    portfolio = 0
                    buyprice = y
                else:
                    shortstock = portfolio / y
                    portfolio = 0
                    buyprice = y

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
        print("portfolio doeks", portfolio)

    x2 = np.array([i for i in range(len(portfoliohistory))])

    profit = []

    for x in portfoliohistory:
        profit.append(x)

    print(profit)
    X_Y_Spline2 = make_interp_spline(x2, portfoliohistory)

    X_2 = np.linspace(x2.min(), x2.max(), 50)
    Y_2 = X_Y_Spline2(X_2)

    X_Y_Spline3 = make_interp_spline(x2, profit)

    Y_3 = X_Y_Spline3(X_2)

    plt.plot(X_2, Y_2)
    plt.plot(X_2, Y_3)
plt.legend(n)
plt.show()

