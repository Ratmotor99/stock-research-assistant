import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder

# Set page layout to wide to make more room for the table
st.set_page_config(layout="wide")

# Set up the Streamlit app title
st.title("Stock Research Assistant")

# Fetch S&P 500 stock symbols from Wikipedia
@st.cache
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
    stock_list = all_stocks
else:
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

# Create interactive Ag-Grid table
gb = GridOptionsBuilder.from_dataframe(stock_data_df)
gb.configure_selection('single')  # Enable row selection
grid_options = gb.build()

st.write("### Stock Data (click to select a stock)")
grid_response = AgGrid(stock_data_df, gridOptions=grid_options)

# Get the selected stock from the Ag-Grid
selected_row = grid_response['selected_rows']

if selected_row:
    selected_symbol = selected_row[0]['Symbol']
    
    # Display selected stock's chart
    stock = yf.Ticker(selected_symbol)
    
    time_period = st.selectbox(
        "Select time range for stock price chart",
        options=["1mo", "3mo", "6mo", "1y", "5y", "max"],
        index=3  # Default to "1y" (1 year)
    )
    
    try:
        stock_data = stock.history(period=time_period)
        if not stock_data.empty:
            st.write(f"### {selected_symbol} Price Chart ({time_period})")
            st.line_chart(stock_data['Close'])  # Line chart of closing prices
        else:
            st.write(f"### {selected_symbol}: No data available for price chart.")
    except Exception as e:
        st.write(f"Error fetching data for {selected_symbol}: {e}")
