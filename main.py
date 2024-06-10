import streamlit as sl
from datetime import date
import yfinance as yahoo
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

sl.title("Stock Prediction Site")

stocks = ("GOOG", "MSFT", "TSLA", "AAPL", "GME", "AMC")
selected_stock = sl.selectbox("Select the stock you want for prediciton", stocks)

num_years = sl.slider("Years of prediction", 1, 10)
period = num_years * 365


def get_data(ticker):
    data = yahoo.download(ticker, START, TODAY)
    # puts date in first column
    data.reset_index(inplace=True)
    return data

data_state = st.text("Loading data...")
data = get_data(selected_stock)