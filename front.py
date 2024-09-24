import streamlit as st
import numpy as np
import requests

st.title("""Auxílio de decisão para venda e compra de criptomoedas""")

st.text("")
st.text("")

add_selectbox = st.selectbox(
    """ # Escolha o cripto ativo que deseja analisar: """,
    ("",'ETH', 'BTC')
)

st.text("")
st.text("")
st.text("")
st.text("")



if add_selectbox == 'ETH':
    with st.spinner("Please wait..."):
        req = requests.get("http://localhost:8000/eth")
    st.write(f"O modelo sugere: {req.text}")
elif add_selectbox == 'BTC':
    with st.spinner("Please wait..."):
        req = requests.get("http://localhost:8000/btc")
    st.write(f"O modelo sugere: {req.text}")

