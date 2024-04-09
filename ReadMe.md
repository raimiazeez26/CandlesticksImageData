# Candle Plot

This project contains code to generate images of candles which can be used to train Neural Network Models for price 
predictions.

The script pulls data from yfinance, split the data into train and test and then generates images of a number of 
price candles and computes the sum of returns after a number of days of the  candle pattern based on input variables 
for the train and test datasets. 

For Example: the script will generate 10 candlestick patterns/formation, then compute the sum of returns after 5 days 
of the candle formation, and assign the image to either Up or Down folder if the sum of returns is positive or negative.

## Parameters 

- Set input parameters for data collection; Asset ticker, start and end dates.
- Set parameters for number of candles to plot  _candle_window_
- Set parameters for number of days after candle data to compute returns _returns_window_
- Set parameter for _test_size_


## Usage
The resulting dataset can be used to train Machine Learning and Neural Network models for price prediction.
Some models you can train for price prediction using images of price candle data include:
- CNN
- RNN
- LSTM

See example usage of image recognition model here:  

