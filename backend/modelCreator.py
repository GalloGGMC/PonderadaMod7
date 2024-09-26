import numpy as np
from datetime import datetime
import yfinance as yf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import json

def createModel(coin: str):

    ticker = yf.Ticker(coin)
    df = ticker.history(period='max', interval='1m')

    df = df.drop(columns=["Dividends","Stock Splits","High","Low","Open","Volume"])
    df = df.rename(columns={"Close":"Value"})
    with open('info.json', 'r') as openfile:
        info = json.load(openfile)
    info[coin]["max"] = df["Value"].max()
    info[coin]["min"] = df["Value"].min()
    info[coin]["maxVol"] = df["Volume"].max()
    with open('info.json', 'w') as outfile:
        json.dump(info, outfile)
    df["Value"] = (df["Value"] - df["Value"].min()) / (df["Value"].max() - df["Value"].min())

    values = df["Value"].values.reshape(-1,1)
    X_train = []
    y_train = []
    for i in range(60, len(df)-3000):
        X_train.append(values[i-60:i, 0])
        y_train.append(values[i, 0])

    X_train, y_train = np.array(X_train), np.array(y_train)

    X_test = []
    y_test = []
    for i in range(len(df)-2940, len(df)):
        X_test.append(values[i-60:i, 0])
        y_test.append(values[i, 0])

    X_test, y_test = np.array(X_test), np.array(y_test)

    model = Sequential()
    model.add(LSTM(units=55,return_sequences=True,input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.15))
    model.add(LSTM(units=55,return_sequences=True))
    model.add(Dropout(0.15))
    model.add(LSTM(units=55,return_sequences=True))
    model.add(Dropout(0.15))
    model.add(LSTM(units=55))
    model.add(Dropout(0.15))
    model.add(Dense(units=1))
    model.compile(optimizer='adam',loss='mean_absolute_error')
    model.fit(X_train,y_train,epochs=100,batch_size=32)

    model.save(f"models/{coin}.h5")
    

if __name__ == "__main__":
    createModel("ETH-USD")
    createModel("BTC-USD")