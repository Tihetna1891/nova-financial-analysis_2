# __init__.py

# Import commonly used libraries and functions for easy access
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import nltk
from nltk.corpus import stopwords
from collections import Counter
from textblob import TextBlob

# Download NLTK stopwords if they haven't been downloaded already
nltk.download('stopwords', quiet=True)