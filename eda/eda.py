import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import nltk
from nltk.corpus import stopwords
from collections import Counter
from textblob import TextBlob

import matplotlib.pyplot as plt
# Load the dataset and inspect the column names
df = pd.read_csv('C:/Users/dell/nova-financial-analysis_2/raw_analyst_ratings.csv')
# print(df.columns)
st.write(df.columns)

# Drop the 'Unnamed: 0' column
df_cleaned = df.drop(columns=['Unnamed: 0'])
# Convert 'date' column to datetime, handling timezones
df_cleaned['date'] = pd.to_datetime(df_cleaned['date'], errors='coerce')

# Verify the conversion
# print(df_cleaned['date'].dtype)
st.write(df_cleaned['date'].dtype)
# Calculate headline lengths
df_cleaned['headline_length'] = df_cleaned['headline'].apply(len)


# Basic statistics on headline lengths
st.write(df_cleaned['headline_length'].describe())

# Count the number of articles per publisher
articles_per_publisher = df_cleaned['publisher'].value_counts()
st.write(articles_per_publisher)

# Analyze publication dates
publication_trends = df_cleaned['date'].dt.date.value_counts().sort_index()
st.write(publication_trends)

# Perform sentiment analysis on headlines
df_cleaned['sentiment'] = df_cleaned['headline'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Check sentiment distribution
st.write(df_cleaned['sentiment'].describe())

nltk.download('stopwords')

# Tokenize and clean headlines
stop_words = set(stopwords.words('english'))
df_cleaned['tokens'] = df_cleaned['headline'].apply(lambda x: [word for word in x.lower().split() if word not in stop_words])

# Count most common words
all_words = [word for tokens in df_cleaned['tokens'] for word in tokens]
word_freq = Counter(all_words)
st.write(word_freq.most_common(10))


# Resample the data by day, week, or month
publication_trends_resampled = publication_trends.resample('Y').sum()  # Weekly aggregation

# Plotting the resampled data
publication_trends_resampled.plot(kind='line', title='Weekly Publication Trends')
plt.xlabel('Week')
plt.ylabel('Number of Articles')

st.pyplot(plt)