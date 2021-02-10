import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt



def calculate_ema(period, lst):
    initial = sum(lst) / period
    mult = 2 / (period + 1)
    emas = [initial]
    for i in range(period, len(lst)):
        new_ema = (lst[i] - emas[-1]) * mult + emas[-1]
        emas.append(new_ema)
    return emas

ticker = 'SNDL'
stonk = yf.Ticker(ticker)
df = stonk.history(period='max')



ema_12 = calculate_ema(12, df['Close'])
ema_26 = calculate_ema(26, df['Close'])
length = min(len(ema_12), len(ema_26))


macds = [a - b for (a, b) in zip(ema_12[-length:], ema_26[-length:])]
signals = calculate_ema(9, macds)

places = 3
print([round(x, places) for x in macds[-5:]], [round(x, places) for x in signals[-5:]])
print(ema_12[-1], ema_26[-1], macds[-1], signals[-1])
price = 351 / 28 * (signals[-1] - 11 / 13 * ema_12[-1] + 25 / 27 * ema_26[-1])
print(price)

rng = 100
diff = [a - b for a, b in zip(macds[-rng:], signals[-rng:])]
fig, ax = plt.subplots(3, 1, figsize=(11,8))
ax[0].set_title(ticker)
ax[0].plot(range(rng),df['Close'][-rng:])
ax[0].grid('on')
ax[1].plot(macds[-rng:])
ax[1].plot(signals[-rng:])
ax[1].grid('on')
ax[2].bar(range(rng), diff)

plt.show()