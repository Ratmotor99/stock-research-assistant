import streamlit as st
import yfinance as yf
import pandas as pd

# Set the page title
st.title("Top Dividend Stock Selector (Testing with 10 Stocks)")

# Step 1: Define a list of 10 dividend-paying stocks for testing
dividend_stocks = ['AAPL', 'MSFT', 'KO', 'PEP', 'T', 'VZ', 'JNJ', 'PG', 'XOM', 'CVX']

# Step 2: Input for selecting the number of top dividend stocks to display
num_top_stocks = st.number_input("How many top dividend stocks to display?", min_value=1, max_value=10, value=5)

# Step 3: Fetch stock data for the predefined list of dividend stocks
stock_data_list = []

for symbol in dividend_stocks:
    stock = yf.Ticker(symbol)
    info = stock.info

    # Only include stocks with non-zero dividend yield
    dividend_yield = info.get('dividendYield', 0)

    if dividend_yield:  # If dividend yield exists
        # Add stock data to the list
        stock_data = {
            'Symbol': symbol,
            'Price': info.get('currentPrice', 'N/A'),
            'Dividend Yield': dividend_yield,
            'Dividend per Share': info.get('dividendRate', 'N/A')
        }
        stock_data_list.append(stock_data)

# Convert to DataFrame
stock_data_df = pd.DataFrame(stock_data_list)

# Sort by dividend yield (highest to lowest)
sorted_stocks = stock_data_df.sort_values(by='Dividend Yield', ascending=False)

# Step 4: Display the top N dividend stocks as specified by the user
top_stocks = sorted_stocks.head(num_top_stocks)

st.write(f"### Top {num_top_stocks} Dividend Stocks")
st.dataframe(top_stocks[['Symbol', 'Price', 'Dividend Yield', 'Dividend per Share']])

# Step 5: Display the chart for each selected stock
for index, row in top_stocks.iterrows():
    symbol = row['Symbol']
    stock = yf.Ticker(symbol)
    stock_data = stock.history(period='1y')

    st.write(f"### {symbol} Price Chart")
    st.line_chart(stock_data['Close'])
