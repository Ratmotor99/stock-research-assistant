import streamlit as st
import yfinance as yf
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.title("Stock Research Assistant")

# Fetch stock symbols
symbols = ['AAPL', 'MSFT', 'GOOG', 'AMZN']  # Example stocks
stock_data_list = []

# Fetch stock data for each symbol
for symbol in symbols:
    stock = yf.Ticker(symbol)
    info = stock.info
    
    stock_data = {
        'Symbol': symbol,
        'Price': info.get('currentPrice', 'N/A'),
        'Market Cap': info.get('marketCap', 'N/A'),
        'P/E Ratio': info.get('trailingPE', 'N/A'),
    }
    
    stock_data_list.append(stock_data)

# Convert list to DataFrame
stock_data_df = pd.DataFrame(stock_data_list)

# Ag-Grid settings
gb = GridOptionsBuilder.from_dataframe(stock_data_df)
gb.configure_selection('single')  # Enable single row selection
grid_options = gb.build()

# Display Ag-Grid table
st.write("### Stock Data Table (Click to select)")
grid_response = AgGrid(stock_data_df, gridOptions=grid_options)

# Get selected row
selected_row = grid_response['selected_rows']

if selected_row:
    selected_symbol = selected_row[0]['Symbol']
    
    # Fetch and display chart for the selected stock
    stock = yf.Ticker(selected_symbol)
    stock_data = stock.history(period='1y')
    
    st.write(f"### {selected_symbol} Price Chart")
    st.line_chart(stock_data['Close'])
