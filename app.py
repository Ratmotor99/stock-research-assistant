import streamlit as st
import yfinance as yf
import pandas as pd

# Set the page title
st.title("Top Dividend Stock Selector")

# Step 1: Fetch S&P 500 stock symbols from Wikipedia
@st.cache
def get_sp500_stocks():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_table = pd.read_html(url, header=0)[0]
    return sp500_table['Symbol'].tolist()

sp500_stocks = get_sp500_stocks()

# Step 2: Predefined ETF symbols
etfs = ['SPY', 'IVV', 'VOO', 'QQQ', 'DIA', 'IWM', 'XLF', 'XLK', 'VTI', 'AGG']  # This can be expanded

# Step 3: Add checkboxes for S&P 500 and ETFs
include_sp500 = st.checkbox("Include S&P 500 Stocks", value=True)
include_etfs = st.checkbox("Include ETFs", value=True)

# Step 4: Create a combined stock list based on user selection
stock_list = []
if include_sp500:
    stock_list.extend(sp500_stocks)
if include_etfs:
    stock_list.extend(etfs)

# Step 5: Input for selecting the number of top dividend stocks to display
num_top_stocks = st.number_input("How many top dividend stocks to display?", min_value=1, max_value=len(stock_list), value=5)

# Fetch stock data and store in a list
stock_data_list = []

if stock_list:
    for symbol in stock_list:
        stock = yf.Ticker(symbol)
        info = stock.info

        # Check if the stock pays dividends (non-zero dividend yield)
        dividend_yield = info.get('dividendYield', 0)
        
        if dividend_yield:  # Only include stocks with non-zero dividend yield
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

# Step 6: Display the top N dividend stocks as specified by the user
top_stocks = sorted_stocks.head(num_top_stocks)

st.write(f"### Top {num_top_stocks} Dividend Stocks")
st.dataframe(top_stocks[['Symbol', 'Price', 'Dividend Yield', 'Dividend per Share']])

# Step 7: Display the chart for each selected stock
for index, row in top_stocks.iterrows():
    symbol = row['Symbol']
    stock = yf.Ticker(symbol)
    stock_data = stock.history(period='1y')

    st.write(f"### {symbol} Price Chart")
    st.line_chart(stock_data['Close'])
