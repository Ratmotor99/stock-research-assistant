
import streamlit as st
import yfinance as yf
import pandas as pd

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
    
    # Store relevant data: Stock symbol, price, dividend yield, dividend per share
    stock_data = {
    'Symbol': symbol,
    'Price': info.get('regularMarketPrice', 'N/A'),
    'Dividend Yield': info.get('dividendYield', 'N/A'),
    'Dividend per Share': info.get('dividendRate', 'N/A'),
    'Market Cap': info.get('marketCap', 'N/A'),
    'P/E Ratio': info.get('trailingPE', 'N/A'),
    '52-Week High': info.get('fiftyTwoWeekHigh', 'N/A'),
    '52-Week Low': info.get('fiftyTwoWeekLow', 'N/A')
}
    
    stock_data_list.append(stock_data)

# Convert the list of dictionaries into a DataFrame
stock_data_df = pd.DataFrame(stock_data_list)

# Display the stock data as a table in Streamlit
st.write("### Stock Data")
st.dataframe(stock_data_df)
