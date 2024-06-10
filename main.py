import streamlit as sl
from datetime import date
import yfinance as yahoo
from prophet import proph
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

sl.title("Stock Prediction Site")

stocks = ("GOOG", "MSFT", "TSLA", "AAPL", "GME", "AMC")
selected_stocks = sl.selectbox("Select the stock you want for prediciton", stocks)

n_years = sl.slider()
