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

# helpful cache decorator for streamlit
@sl.cache_data
def get_data(ticker):
    # this data is a pandas dataframe
    data = yahoo.download(ticker, START, TODAY)
    # puts date in first column
    data.reset_index(inplace=True)
    return data

def plot_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    sl.plotly_chart(fig)

data_state = sl.text("Loading data...")
data = get_data(selected_stock)
data_state.text("Loaded data!")

sl.subheader("Raw stock data")
sl.write(data.tail())

plot_data(data)

# prediction using prophet
df_train = data[['Date', 'Close']]

# how prophet takes the data, look at documentation
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

# init prophet model and start training
model = Prophet()
model.fit(df_train)
future = model.make_future_dataframe(periods=period)
prediction = model.predict(future)

sl.subheader("Prediction data")
sl.write(prediction.tail())

sl.write('Prediction data')
fig1 = plot_plotly(model, prediction)
sl.plotly_chart(fig1)

sl.write('Prediction components')
fig2 = model.plot_components(prediction)
# not a plot so dont need to plotly plot
sl.write(fig2)