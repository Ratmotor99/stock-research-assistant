import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Set page layout to wide to make more room for the table
st.set_page_config(layout="wide")

# Set up the Streamlit app title
st.title("Stock Research Assistant")

# Fetch S&P 500 stock symbols from Wikipedia
@st.cache  # Cache the result to avoid reloading on every run
def get_sp500_stocks():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_table = pd.read_html(url, header=0)[0]
    return sp500_table['Symbol'].tolist()

sp500_stocks = get_sp500_stocks()

# Predefined ETF symbols
etfs = ['SPY', 'IVV', 'VOO', 'QQQ', 'DIA', 'IWM', 'XLF', 'XLK', 'VTI', 'AGG']

# Combine S&P 500 stocks and ETFs into one list
all_stocks = sp500_stocks + etfs

# Show only the first 10 stocks initially
initial_stocks = all_stocks[:10]

# Add a checkbox to show all stocks and ETFs
show_all = st.checkbox("Show all S&P 500 and ETF symbols")

if show_all:
    # If checkbox is selected, show all stocks and ETFs
    stock_list = all_stocks
else:
    # Otherwise, show only the first 10 stocks
    stock_list = initial_stocks

# Create an empty list to hold stock data
stock_data_list = []

# Fetch data for each selected stock symbol
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

# Display the stock data as a wider table
st.write("### Stock Data")
st.dataframe(stock_data_df, width=1200)

# Create a checkbox for each stock to select it for displaying the chart
st.write("### Select Stocks for Chart Display")
selected_stocks = []
for symbol in stock_list:
    # Add a checkbox for each stock symbol
    if st.checkbox(f"Select {symbol} for chart"):
        selected_stocks.append(symbol)

# If no stocks are selected, show a message
if not selected_stocks:
    st.write("No stocks selected for chart display.")
else:
    # Create a selectbox for the time range of the charts
    time_period = st.selectbox(
        "Select time range for stock price charts",
        options=["1mo", "3mo", "6mo", "1y", "5y", "max"],
        index=3  # Default to "1y" (1 year)
    )

    # Display line charts only for the selected stocks/ETFs
    st.write(f"### Stock Price Trends for {time_period} Period")
    for symbol in selected_stocks:
        stock = yf.Ticker(symbol)
        
        # Error handling: Check if stock data is available
        try:
            stock_data = stock.history(period=time_period)  # Fetch data for the selected time period
            if not stock_data.empty:
                # Display the line chart for the stock's closing prices
                st.write(f"### {symbol} Price Chart ({time_period})")
                st.line_chart(stock_data['Close'])  # Line chart of closing prices
            else:
                st.write(f"### {symbol}: No data available for price chart.")
        except Exception as e:
            st.write(f"Error fetching data for {symbol}: {e}")
