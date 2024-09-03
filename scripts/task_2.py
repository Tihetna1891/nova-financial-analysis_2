import pandas as pd
import os
import talib as ta
import pynance as pn
import matplotlib.pyplot as plt
import streamlit as st
# Define the directory where your CSV files are stored
directory = "C:/Users/dell/Downloads/yfinance_data/yfinance_data"

# Create an empty dictionary to hold the DataFrames
stock_data = {}

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv") or filename.endswith(".xls") or filename.endswith(".xlsx"):
        # Create the full file path
        file_path = os.path.join(directory, filename)
        
        # Extract the stock symbol from the filename (assuming the format is "SYMBOL_historical_data.csv")
        stock_symbol = filename.split('_')[0]
        
        # Load the data into a DataFrame (choose method based on file type)
        df = pd.read_excel(file_path) if filename.endswith(('.xls', '.xlsx')) else pd.read_csv(file_path)
        
        # Store the DataFrame in the dictionary with the stock symbol as the key
        stock_data[stock_symbol] = df

# Check if the necessary columns are present in each DataFrame
required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']

for symbol, df in stock_data.items():
    if all(col in df.columns for col in required_columns):
        print(f"{symbol} data includes all required columns.")
    else:
        missing_cols = [col for col in required_columns if col not in df.columns]
        print(f"{symbol} data is missing the following columns: {missing_cols}")

# Function to add TA-Lib indicators to each DataFrame
def add_ta_indicators(df):
    df['SMA'] = ta.SMA(df['Close'], timeperiod=14)
    df['EMA'] = ta.EMA(df['Close'], timeperiod=14)
    df['RSI'] = ta.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

# Function to calculate returns and volatility
def add_financial_metrics(df):
    df['Returns'] = df['Close'].pct_change()
    df['Volatility'] = df['Returns'].rolling(window=21).std()

# Function to plot data using Streamlit
def plot_stock_data(symbol, df):
    st.subheader(f'{symbol} - Stock Data and Technical Indicators')

    # Plot Close Price with SMA and EMA
    st.line_chart(df[['Close', 'SMA', 'EMA']])
    
    # Plot RSI
    st.line_chart(df[['RSI']])
    
    # Plot MACD
    st.line_chart(df[['MACD', 'MACD_Signal']])
    
    # Show MACD Histogram as a bar chart
    st.bar_chart(df[['MACD_Hist']])

    # Show Returns and Volatility
    st.line_chart(df[['Returns', 'Volatility']])

# Load data and apply indicators
@st.cache_data
def load_and_process_data(file_path):
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    add_ta_indicators(df)
    add_financial_metrics(df)
    return df

# Streamlit UI
st.title('Financial Data Analysis with Technical Indicators')

# Select stock data file
file_options = {
    "AAPL": "AAPL_historical_data.csv",
    "AMZN": "AMZN_historical_data.csv",
    "GOOG": "GOOG_historical_data.csv",
    "META": "META_historical_data.csv",
    "MSFT": "MSFT_historical_data.csv",
    "NVDA": "NVDA_historical_data.csv",
    "TSLA": "TSLA_historical_data.csv",
}

selected_stock = st.selectbox("Select a stock to analyze:", list(file_options.keys()))

if selected_stock:
    file_path = os.path.join(directory, file_options[selected_stock])
    df = load_and_process_data(file_path)
    plot_stock_data(selected_stock, df)