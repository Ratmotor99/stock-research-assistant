import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Set up the Streamlit app title
st.title("Stock Research Assistant")

# User input for multiple stock symbols
symbols = st.text_input("Enter stock symbols (comma-separated)", "AAPL, MSFT, KO, JNJ, PFE")

# Convert the input string into a list of stock symbols
stock_list = [symbol.strip() for symbol in symbols.split(",")]

# Create an empty list to hold stock data
stock_data_list = []

# Fetch data for each stock symbol
for symbol in stock_list:
    stock = yf.Ticker(symbol)
    info = stock.info
    
    # Store relevant data: Stock symbol, price, dividend yield, dividend per share, market cap, P/E ratio, 52-week high/low
    stock_data = {
        'Symbol': symbol,
        'Price': info.get('regularMarketPrice', np.nan),  # Convert 'N/A' to np.nan for proper numerical handling
        'Dividend Yield': info.get('dividendYield', np.nan),
        'Dividend per Share': info.get('dividendRate', np.nan),
        'Market Cap': info.get('marketCap', np.nan),
        'P/E Ratio': info.get('trailingPE', np.nan),
        '52-Week High': info.get('fiftyTwoWeekHigh', np.nan),
        '52-Week Low': info.get('fiftyTwoWeekLow', np.nan)
    }
    
    stock_data_list.append(stock_data)

# Convert the list of dictionaries into a DataFrame
stock_data_df = pd.DataFrame(stock_data_list)

# Display the stock data as a table in Streamlit
st.write("### Stock Data")
st.dataframe(stock_data_df)
