import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from fastapi import FastAPI
from modelCreator import createModel
from tensorflow import keras
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import json

def process_data(coin: str):
    ticker = yf.Ticker(coin)

    df = ticker.history(period="1d", interval='1m')
    df = df.drop(columns=["Dividends","Stock Splits","High","Low","Open"])
    df = df.rename(columns={"Close":"Value"})

    with open('info.json', 'r') as openfile:
        info = json.load(openfile)

    df["Value"] = (df["Value"] - info[coin]["min"])/(info[coin]["max"] - info[coin]["min"])
    values = df["Value"].values.reshape(-1,1)
    x_p = np.array([values[-60+i] for i in range(60)]).reshape(1,60)

    vol = df["Volume"].values[-1]

    return [x_p, vol]

def comparator(arr: list, vol:int, coin: str):
    with open('info.json', 'r') as openfile:
        info = json.load(openfile)

    if arr[0] > 0.1 and arr[1] > 0.1 and vol/info[coin]["maxVol"] < 0.1:
        return "Compre"
    
    elif arr[0] < -0.1 and arr[1] < -0.1 and vol/info[coin]["maxVol"] > 0.2:
        return "Venda"
    
    else:
        return "Aguarde"
    
app = FastAPI()

@app.get("/eth")
def predictETH():
    with open('logs.json', 'r') as openfile:
        log = json.load(openfile)
    log["typeConsult"].append("Predicao Etherium")
    log["date"].append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    with open('logs.json', 'w') as outfile:
        json.dump(log, outfile)

    model = keras.models.load_model("models/ETH-USD.h5")
    X, vol = process_data("ETH-USD")
    y = model.predict(X)
    delta = [(X[0][-1] - X[0][-2])*10, (X[0][-1]-y[0][0])*10]

    return comparator(delta, vol, "ETH-USD")

@app.get("/btc")
def predictETH():
    with open('logs.json', 'r') as openfile:
        log = json.load(openfile)
    log["typeConsult"].append("Predicao Bitcoin")
    log["date"].append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    with open('logs.json', 'w') as outfile:
        json.dump(log, outfile)

    model = keras.models.load_model("models/BTC-USD.h5")
    X, vol = process_data("BTC-USD")
    y = model.predict(X)
    delta = [(X[0][-1] - X[0][-2])*10, (X[0][-1]-y[0][0])*10]

    return comparator(delta, vol, "BTC-USD")

@app.get("/hist_eth")
def histETH():
    with open('logs.json', 'r') as openfile:
        log = json.load(openfile)
    log["typeConsult"].append("Historico Etherium")
    log["date"].append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    with open('logs.json', 'w') as outfile:
        json.dump(log, outfile)

    ticker = yf.Ticker("ETH-USD")
    df = ticker.history(period="5d", interval='1m')
    df = df.drop(columns=["Dividends","Stock Splits","High","Low","Open","Volume"])
    df = df.rename(columns={"Close":"Value"})
    df.index = df.index.strftime("%d/%m/%Y %H:%M:%S")
    j = df.to_json(orient='index')
    parsed = json.loads(j)

    return parsed

@app.get("/hist_btc")
def histBTC():
    with open('logs.json', 'r') as openfile:
        log = json.load(openfile)
    log["typeConsult"].append("Historico Bitcoin")
    log["date"].append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    with open('logs.json', 'w') as outfile:
        json.dump(log, outfile)

    ticker = yf.Ticker("BTC-USD")
    df = ticker.history(period="5d", interval='1m')
    df = df.drop(columns=["Dividends","Stock Splits","High","Low","Open","Volume"])
    df = df.rename(columns={"Close":"Value"})
    df.index = df.index.strftime("%d/%m/%Y %H:%M:%S")
    j = df.to_json(orient='index')
    parsed = json.loads(j)

    return parsed

@app.get("/logs")
def logs():
    with open('logs.json', 'r') as openfile:
        log = json.load(openfile)
    log["typeConsult"].append("Logs")
    log["date"].append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    with open('logs.json', 'w') as outfile:
        json.dump(log, outfile)


    return log

with open("retrain.json", "r") as openfile:
    retrain = json.load(openfile)

if datetime.strptime(retrain["date"], "%d/%m/%Y %H:%M:%S") - datetime.now() > timedelta(days=7):
    createModel("ETH-USD")
    createModel("BTC-USD")
    retrain["date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("retrain.json", "w") as outfile:
        json.dump(retrain, outfile)