# Machine Learning Trading Bot

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import datetime as dt
import pandas_datareader.data as web
from matplotlib import style
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

style.use("ggplot")

start = dt.datetime(2000, 1, 1)
end = dt.datetime(2016, 12, 31)

df = web.DataReader("TSLA", "yahoo", start, end)
df.to_csv("tsla.csv")

df = pd.read_csv("tsla.csv", parse_dates=True, index_col=0)

df["100ma"] = df["Adj Close"].rolling(window=100, min_periods=0).mean()

ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
ax1.plot(df.index, df["Adj Close"])
ax1.plot(df.index, df["100ma"])
ax2.bar(df.index, df["Volume"])

plt.show()

dfreg = df.loc[:, ["Adj Close", "Volume"]]
dfreg["HL_PCT"] = (df["High"] - df["Low"]) / df["Close"] * 100.0
dfreg["PCT_change"] = (df["Close"] - df["Open"]) / df["Open"] * 100.0

dfreg.fillna(value=-99999, inplace=True)

forecast_out = int(math.ceil(0.01 * len(dfreg)))
forecast_col = "Adj Close"
dfreg["label"] = dfreg[forecast_col].shift(-forecast_out)

X = np.array(dfreg.drop(["label"], 1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]

dfreg.dropna(inplace=True)
y = np.array(dfreg["label"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = LinearRegression(n_jobs=-1)
clf.fit(X_train, y_train)
confidence = clf.score(X_test, y_test)

forecast_set = clf.predict(X_lately)
dfreg["Forecast"] = np.nan

last_date = dfreg.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = dt.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    dfreg.loc[next_date] = [np.nan for _ in range(len(dfreg.columns) - 1)] + [i]

dfreg["Adj Close"].plot()
dfreg["Forecast"].plot()
plt.legend(loc=4)
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()

# Path: showcase.py
# Machine Learning Trading Bot
