import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Set page title
st.title("Enhanced Dividend Stock Selector")

# Step 1: Define 10 dividend-paying stocks for testing
dividend_stocks = ['AAPL', 'MSFT', 'KO', 'PEP', 'T', 'VZ', 'JNJ', 'PG', 'XOM', 'CVX']
etfs = ['SPY', 'IVV', 'VOO', 'QQQ', 'DIA']

# Step 2: Add checkboxes for showing dividend stocks and ETFs
show_dividend_stocks = st.checkbox("Show Dividend Stocks", value=True)
show_etfs = st.checkbox("Show ETFs", value=False)

# Step 3: Create stock list based on user selection
stock_list = []
if show_dividend_stocks:
    stock_list.extend(dividend_stocks)
if show_etfs:
    stock_list.extend(etfs)

# Step 4: Input for total investment amount
investment_amount = st.number_input("Enter the amount you want to invest ($)", min_value=100.0, value=1000.0)

# Fetch stock data for the selected stocks
stock_data_list = []

for symbol in stock_list:
    stock = yf.Ticker(symbol)
    info = stock.info

    # Calculate if the stock is up or down today (for color coding)
    current_price = info.get('regularMarketPrice', 0)
    previous_close = info.get('regularMarketPreviousClose', 0)
    price_up = current_price > previous_close  # True if price is up, False if down

    # Calculate the number of years the company has been paying dividends
    dividend_rate = info.get('dividendRate', 0)
    dividend_yield = info.get('dividendYield', 0)
    
    if dividend_rate > 0:
        dividend_start_date = info.get('firstTradeDateEpochUtc', None)
        if dividend_start_date:
            years_paying_dividends = (datetime.datetime.now() - datetime.datetime.fromtimestamp(dividend_start_date)).days // 365
        else:
            years_paying_dividends = 'N/A'
    else:
        years_paying_dividends = 'N/A'

    # Only include dividend-paying stocks
    if dividend_yield:
        stock_data = {
            'Symbol': symbol,
            'Price': f"${current_price:.2f}" if current_price else 'N/A',
            'Dividend Yield (%)': f"{dividend_yield * 100:.2f}%" if dividend_yield else 'N/A',
            'Dividend per Share': f"${dividend_rate:.2f}" if dividend_rate else 'N/A',
            'Years Paying Dividends': years_paying_dividends,
            'Price Up': price_up,  # Track whether the price is up or down for color coding
        }
        stock_data_list.append(stock_data)

# Convert stock data to a DataFrame
stock_data_df = pd.DataFrame(stock_data_list)

# Sort by dividend yield (highest to lowest)
sorted_stocks = stock_data_df.sort_values(by='Dividend Yield (%)', ascending=False)

# Step 5: Calculate the number of shares to buy for each stock based on the investment amount
def calculate_shares(price):
    try:
        return int(investment_amount / float(price.strip('$')))
    except (ValueError, ZeroDivisionError):
        return 'N/A'  # Return 'N/A' if there's an issue with the price

if not sorted_stocks.empty:
    sorted_stocks['Shares to Buy'] = sorted_stocks['Price'].apply(lambda x: calculate_shares(x))

# Step 6: Display the stock data in an autosized table
st.write(f"### Top Dividend Stocks (Showing {len(stock_list)} stocks)")
st.dataframe(sorted_stocks)

# Step 7: Display the chart for each selected stock
for index, row in sorted_stocks.iterrows():
    symbol = row['Symbol']
    stock = yf.Ticker(symbol)
    stock_data = stock.history(period='1y')

    # Show stock price chart
    st.write(f"### {symbol} Price Chart")
    st.line_chart(stock_data['Close'])

    # Step 8: Apply color to the price box (green if price is up, red if down)
    if row['Price Up']:
        st.markdown(f"<span style='color:green'>Price: {row['Price']}</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color:red'>Price: {row['Price']}</span>", unsafe_allow_html=True)
