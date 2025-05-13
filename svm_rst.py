import numpy as np
from sklearn.svm import LinearSVC, SVC
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import ParameterGrid
import yfinance as yf
import datetime as dt
import pandas as pd


def fetch_data(symbol, start, end):
    ticker = yf.download(symbol, start, end)
    return pd.DataFrame(ticker)

def calculate_rsi(data, period = 14):