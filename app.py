import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from raindrop import make_raindrop_chart

st.set_page_config(layout="wide", page_title="Raindrop Charts")
tickers = pd.read_csv("tickers.csv")
st.title("Raindrop Charts using Yfinance, Streamlit, & Plotly")

today = pd.Timestamp.now()
date = st.sidebar.date_input(label="Date Range", value=today)
company = st.sidebar.selectbox(label="Company", options=tickers["Company"])
vwap_margin = st.sidebar.number_input(label="VWAP Margin", value=0.1, step=0.01, min_value=0., format="%.2f")
frequency = st.sidebar.number_input(label="Bin Size (minutes)", value=30, step=1, min_value=5, max_value=60)
ticker = tickers.loc[tickers["Company"] == company, "Ticker"].values[0]
if pd.Timestamp(date) >= pd.Timestamp.now().floor("d"):
    count = st_autorefresh(interval=5000, limit=100, key="fizzbuzzcounter")
raindrop_chart, vwap_open, vwap_close, ohlc = make_raindrop_chart(
    ticker=ticker,
    start=date.strftime("%Y-%m-%d"),
    end=(date + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
    interval="1m",
    frequency_value=frequency,
    margin=vwap_margin
)
col1, col2, col3 = st.columns(3)
col1.metric("VWAP (Current vs Previous)", f"{str(vwap_close)}$", f"{str(vwap_close - vwap_open)}$")
col2.metric("Current Prices (Close vs Open)", f"{str(ohlc['Close'])}$", f"{str(ohlc['Close'] - ohlc['Open'])}$")
col3.metric("Last Update", str(pd.Timestamp.now().floor("s")))
st.plotly_chart(raindrop_chart, use_container_width=True)
