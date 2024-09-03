import pandas as pd
from textblob import TextBlob
import streamlit as st
from dateutil import parser

# Define file paths for each stock
file_options = {
    "AAPL": "C:/Users/dell/Downloads/yfinance_data/yfinance_data/AAPL_historical_data.csv",
    "AMZN": "C:/Users/dell/Downloads/yfinance_data/yfinance_data/AMZN_historical_data.csv",

    "AMZN": "C:/Users/dell/Downloads/yfinance_data/yfinance_data/AMZN_historical_data.csv",
    "GOOG": "C:/Users/dell/Downloads/yfinance_data/yfinance_data/GOOG_historical_data.csv",
    "META": "C:/Users/dell/Downloads/yfinance_data/yfinance_data/META_historical_data.csv",
    "MSFT": "C:/Users/dell/Downloads/yfinance_data/yfinance_data/MSFT_historical_data.csv",
    "NVDA": "C:/Users/dell/Downloads/yfinance_data/yfinance_data/NVDA_historical_data.csv",
    "TSLA": "C:/Users/dell/Downloads/yfinance_data/yfinance_data/TSLA_historical_data.csv"
    # Add more stocks as needed
}

# Load the news dataset
news_file_path = "C:/Users/dell/Downloads/raw_analyst_ratings.csv"
news_df = pd.read_csv(news_file_path)

# Function to parse dates with mixed formats
# def parse_dates(date_str):
#     try:
#         return pd.to_datetime(date_str, format="%Y-%m-%d %H:%M:%S").date()
#     except ValueError:
#         return pd.to_datetime(date_str, format="%m/%d/%Y").date()
def parse_dates(date_str):
    try:
        return parser.parse(date_str).date()
    except ValueError:
        return None  # If parsing fails, return None

# Apply the date parsing function to the news dataset
news_df['date'] = news_df['date'].apply(parse_dates)

# Convert the date column in the news dataset to datetime
# news_df['date'] = pd.to_datetime(news_df['date']).dt.date

# Function to perform sentiment analysis on news headlines
def get_sentiment(headline):
    analysis = TextBlob(headline)
    return analysis.sentiment.polarity

# Apply sentiment analysis to the headlines in the news dataset
news_df['sentiment_score'] = news_df['headline'].apply(get_sentiment)

# Iterate through each stock in the file_options dictionary
for stock, path in file_options.items():
    # Load the stock prices dataset
    stock_df = pd.read_csv(path)
    
    # Convert the date column in the stock dataset to datetime and normalize to date only
    stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.date
    
    # Calculate daily returns for the stock
    stock_df['daily_return'] = stock_df['Close'].pct_change()
    
    # Merge the news sentiment scores with the stock returns by date
    merged_df = pd.merge(news_df, stock_df, left_on='date', right_on='Date', how='inner')
    
    # Calculate the Pearson correlation between sentiment scores and stock returns
    correlation = merged_df['sentiment_score'].corr(merged_df['daily_return'])
    
    # Print the correlation for the current stock
    st.write(f'{stock}: Correlation between sentiment and stock returns: {correlation}')

