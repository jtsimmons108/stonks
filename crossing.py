import yfinance as yf
import pandas as pd


def calculate_ema(period, lst):
    initial = sum(lst) / period
    mult = 2 / (period + 1)
    emas = [initial]
    for i in range(period, len(lst)):
        new_ema = (lst[i] - emas[-1]) * mult + emas[-1]
        emas.append(new_ema)
    return emas

ticker = 'SNDL'
df = yf.download(ticker )

vals = df['Close'].tolist()
ema_12 = calculate_ema(12, vals)
ema_26 = calculate_ema(26, vals)
length = min(len(ema_12), len(ema_26))

target = (27 * ema_12[-1] - 13 * ema_26[-1]) / 14
print(target)
macds = [a - b for (a, b) in zip(ema_12[-length:], ema_26[-length:])]
signals = calculate_ema(9, macds)
print(macds[-1])
print(signals[-1])
print(macds[-1] - signals[-1])
price = 351 / 28 * (signals[-1] - 11 / 13 * ema_12[-1] + 25 / 27 * ema_26[-1])
print(price)