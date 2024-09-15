import streamlit as st
import yfinance as yf
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Set up the Streamlit app title
st.title("Stock Research Assistant")

# Sample stock symbols (you can replace these with any other stocks)
symbols = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']

# Create an empty list to store stock data
stock_data_list = []

# Fetch stock data for each symbol
for symbol in symbols:
    stock = yf.Ticker(symbol)
    info = stock.info
    
    # Extract relevant stock data (price, P/E ratio, market cap, etc.)
    stock_data = {
        'Symbol': symbol,
        'Price': info.get('currentPrice', 'N/A'),
        'Market Cap': info.get('marketCap', 'N/A'),
        'P/E Ratio': info.get('trailingPE', 'N/A'),
        'Dividend Yield': info.get('dividendYield', 'N/A'),
        '52-Week High': info.get('fiftyTwoWeekHigh', 'N/A'),
        '52-Week Low': info.get('fiftyTwoWeekLow', 'N/A')
    }
    
    stock_data_list.append(stock_data)

# Convert stock data list to DataFrame
stock_data_df = pd.DataFrame(stock_data_list)

# Create Ag-Grid settings to make the table interactive
gb = GridOptionsBuilder.from_dataframe(stock_data_df)
gb.configure_selection('single')  # Enable single-row selection
grid_options = gb.build()

# Display the stock data table using Ag-Grid
st.write("### Stock Data Table (Click to select a stock)")
grid_response = AgGrid(stock_data_df, gridOptions=grid_options)

# Get the selected row from the table
selected_row = grid_response['selected_rows'] if grid_response else None

# Check if any row is selected and handle NoneType
if selected_row and len(selected_row) > 0:
    selected_symbol = selected_row[0]['Symbol']
    
    # Fetch and display the chart for the selected stock
    stock = yf.Ticker(selected_symbol)
    stock_data = stock.history(period='1y')  # Fetch 1-year data
    
    st.write(f"### {selected_symbol} Price Chart")
    st.line_chart(stock_data['Close'])
else:
    st.write("No stock selected.")
