# IMPORT LIBRARIES
import warnings

warnings.filterwarnings('ignore')
from datetime import date
import yfinance as yf
import plotly.graph_objects as go
import os

# Creating your directories
folder_names = ["Train", "Train/Up", "Train/Down", "Test", "Test/Up", "Test/Down"]
[os.mkdir(folder) for folder in folder_names if not os.path.exists(folder)]


# Pull asset data from yfinance
def get_data(ticker, start, end):
    start_date = start  # '1990-01-01'
    end_date = end  # str(date.today())
    INTERVAL = '1d'  # granularity of historical data

    data = yf.download(ticker, start_date, end_date, INTERVAL)
    data.columns = data.columns.str.capitalize()

    return data.dropna()


# plot CANDLES
def generate_plot(stock_data, ticker, index, path):
    df = stock_data.reset_index()
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])

    fig.update_layout(
        # height=1200,
        showlegend=False,
        yaxis={'side': 'right'},
        margin=dict(l=1, r=1, t=1, b=1),
    )
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)')
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_xaxes(showgrid=False, showspikes=True, rangebreaks=[
        dict(bounds=["sat", "mon"])  # hide weekends
    ])

    fig.update_layout(xaxis={'visible': False, 'showticklabels': False})
    fig.update_layout(yaxis={'visible': False, 'showticklabels': False})

    fig.write_image(f"{path}/{ticker}_{index}.png")


# generate TRAIN DATA plots for every 'candle_window' data chunk
def generate_train(train_data, data, candle_window, returns_window):
    index = 0
    ticker = train_data['Ticker'].unique()[0]

    # Iterate over the dataset in chunks of 'candle_window' rows
    for i in range(0, len(train_data), candle_window):
        chunk = train_data.iloc[i:i + candle_window]
        returns_data = data.iloc[i + candle_window:i + candle_window + returns_window]

        if len(chunk) == candle_window:
            if sum(returns_data['returns']) > 0:
                path = 'Train/Up'
                generate_plot(chunk, ticker, index, path)
                index += 1

            else:
                path = 'Train/Down'
                generate_plot(chunk, ticker, index, path)
                index += 1
        else:
            pass


# generate TRAIN DATA plots for every 'candle_window' data chunk
def generate_test(test_data, data, candle_window, returns_window):
    index = 0
    ticker = test_data['Ticker'].unique()[0]

    # Iterate over the dataset in chunks of 'candle_window' rows
    for i in range(0, len(test_data), candle_window):
        chunk = test_data.iloc[i:i + candle_window]
        returns_data = data.iloc[i + candle_window:i + candle_window + returns_window]

        if len(chunk) == candle_window:
            if sum(returns_data['returns']) > 0:
                path = 'Test/Up'
                generate_plot(chunk, ticker, index, path)
                index += 1

            else:
                path = 'Test/Down'
                generate_plot(chunk, ticker, index, path)
                index += 1

        else:
            pass


def generate_candle_images(tickers, start, end, candle_window, returns_window, test_size):
    # Pull asset data
    data_list = []
    for ticker in tickers:
        data = get_data(ticker, start, end)
        data['returns'] = data['Close'].pct_change()
        data['Ticker'] = ticker

        data_list.append(data)

    for data in data_list:
        # Split train test data
        train_size_value = int(len(data)*test_size)
        train_size = len(data) - train_size_value

        test_data = data.iloc[-train_size_value:]
        train_data = data.iloc[:train_size]

        # Generate candle plots from data
        generate_train(train_data, data, candle_window, returns_window)
        generate_test(test_data, data, candle_window, returns_window)


# set parameters
tickers = ['QQQ', 'SPY'] # Assets ticker
start = '1980-01-01' # start date
end = str(date.today()) # end date
candle_window = 10 # number of candles to plot
returns_window = 5 # number of days after candle data to check returns
test_size = 0.20 # size of test data

if __name__ == '__main__':
    generate_candle_images(tickers, start, end, candle_window, returns_window, test_size)