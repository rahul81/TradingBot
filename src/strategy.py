import pandas as pd
import numpy as np

import talib

import matplotlib.pyplot as plt
from matplotlib import style

style.use("seaborn")


df = pd.read_csv("data/NIFTY.csv", parse_dates=["Date"])
df = df[["Date", "Close"]]

df["EMA8"] = talib.EMA(df["Close"], 8)
df["EMA13"] = talib.EMA(df["Close"], 13)
df["EMA21"] = talib.EMA(df["Close"], 21)
df["EMA55"] = talib.EMA(df["Close"], 55)
# print(df.dropna().head(20))

df["positions"] = -1

df.loc[
    (df["EMA8"] > df["EMA55"])
    & (df["EMA13"] > df["EMA55"])
    & (df["EMA21"] > df["EMA55"]),
    "positions",
] = 1

df = df.dropna()[:1000].reset_index(drop=True)

print(df.head())

fig, ax1 = plt.subplots(figsize=(15, 8))
ax2 = ax1.twinx()
ax1.plot(df["Close"], color="black", label="Nifty")
ax1.plot(df["EMA8"], color="blue", label="EMA8")
ax1.plot(df["EMA13"], color="green", label="EMA13")
ax1.plot(df["EMA21"], color="yellow", label="EMA21")
ax1.plot(df["EMA55"], color="red", label="EMA55")
ax2.plot(df["positions"], label="positions")
ax2.grid(False)
plt.tight_layout()
ax1.legend()
ax2.legend(loc="upper right")
plt.savefig("images/4EMA.png")
plt.show()
