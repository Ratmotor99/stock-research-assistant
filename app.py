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
    
    # Use 'currentPrice' as the stock price field
    price = info.get('currentPrice', np.nan)
    
    # Store relevant data: Stock symbol, price, dividend yield, dividend per share, market cap, P/E ratio, 52-week high/low
    stock_data = {
        'Symbol': symbol,
        'Price': price,
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

# Create a multiselect box to let users choose which stocks they want to display charts for
selected_stocks = st.multiselect(
    "Select stocks to display charts",
    options=stock_list,
    default=stock_list  # Pre-select all stocks initially
)

# Display line charts only for the selected stocks
st.write("### Stock Price Trends")
for symbol in selected_stocks:
    stock = yf.Ticker(symbol)
    
    # Error handling: Check if stock data is available
    try:
        stock_data = stock.history(period="1y")  # Fetch 1 year of data
        if not stock_data.empty:
            # Display the line chart for the stock's closing prices
            st.write(f"### {symbol} Price Chart (1 Year)")
            st.line_chart(stock_data['Close'])  # Line chart of closing prices
        else:
            st.write(f"### {symbol}: No data available for price chart.")
    except Exception as e:
        st.write(f"Error fetching data for {symbol}: {e}")
