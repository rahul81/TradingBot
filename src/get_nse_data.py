from nsepy import get_history
import datetime

import pandas as pd
import os


def get_data():
    start = datetime.date(2000, 1, 1)
    end = datetime.date.today()

    symbol = "NIFTY"

    data = get_history(symbol, start, end, index=True)

    data.to_csv("data/NIFTY.csv", index=True)


def resample(debug=False):
    path = "data/NIFTY.csv"
    if os.path.exists(path):
        df = pd.read_csv(path, parse_dates=["Date"])
    else:
        get_data()
        df = pd.read_csv(path, parse_dates=["Date"])

    df = df.set_index("Date")
    df = df.resample("1D").mean().dropna()

    df = df[["Open", "Close", "High", "Low", "Volume"]]

    five_d_obs = []
    thirty_d_obs = []
    sixty_d_obs = []

    for i in range(df.shape[0]):
        c = 0
        sum5 = 0
        if i < len(df) - 5:
            while c < 5:
                sum5 += df["Close"][c]
                c += 1

            if sum5 / 5 > df["Close"][i]:
                five_d_obs.append(1)
            else:
                five_d_obs.append(0)
        else:
            five_d_obs.append(0)

        c = 0
        sum30 = 0
        if i < len(df) - 30:
            while c < 30:
                sum30 += df["Close"][c]
                c += 1
            if sum30 / 30 > df["Close"][i]:
                thirty_d_obs.append(1)
            else:
                thirty_d_obs.append(0)
        else:
            thirty_d_obs.append(0)

        c = 0
        sum60 = 0
        if i < len(df) - 60:
            while c < 60:
                sum60 += df["Close"][c]
                c += 1
            if sum60 / 60 > df["Close"][i]:
                sixty_d_obs.append(1)
            else:
                sixty_d_obs.append(0)
        else:
            sixty_d_obs.append(0)

    df["five_d_obs"] = five_d_obs
    df["thirty_d_obs"] = thirty_d_obs
    df["sixty_d_obs"] = sixty_d_obs
    if debug:
        print(df.head())
    return df.dropna()
