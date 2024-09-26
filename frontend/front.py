import streamlit as st
import numpy as np
import requests
import pandas as pd

st.set_page_config(
        page_title="Ponderada Módulo 7",
)
st.title("Auxílio de decisão para venda e compra de criptomoedas")

st.text("")
st.text("")

with st.spinner("Carregando dados de Etherium..."):
    et = requests.get("http://server:8000/hist_eth")
    req_et = requests.get("http://server:8000/eth")
    df_eth = pd.DataFrame.from_dict(et.json(), orient='index')

with st.spinner("Carregando dados de Bitcoin..."):
    bt = requests.get("http://server:8000/hist_btc")
    req_bt = requests.get("http://server:8000/btc")
    df_btc = pd.DataFrame.from_dict(bt.json(), orient='index')

with st.spinner("Carregando logs..."):
    logs = requests.get("http://server:8000/logs")
    df_logs = pd.DataFrame.from_dict(logs.json(), orient='index')
    df_logs = df_logs.transpose()
    df_logs = df_logs.rename(columns={"typeConsult":"Tipo de Consulta", "date":"Data"})
    df_logs.index = df_logs["Data"]
    df_logs = df_logs.drop(columns=["Data"])
    df_logs = df_logs.transpose()
    

left_column, right_column = st.columns(2)

left_column.write("## Etherium")
right_column.write("## Bitcoin")

left_column.line_chart(df_eth, use_container_width=True)
right_column.line_chart(df_btc , use_container_width=True)

st.text("")
st.text("")

left_column.write(f"O modelo sugere (ETH): {req_et.text}")
right_column.write(f"O modelo sugere (BTC): {req_et.text}")

st.text("")

st.write("## Logs")
st.text("")
st.write(df_logs)






    

