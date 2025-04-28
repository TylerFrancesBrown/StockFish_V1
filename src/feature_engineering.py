import pandas as pd
import numpy as np

def create_features(df, lags=[1,5,10], windows=[5,10,20]):
    # 1) Compute log returns
    df = df.copy()
    df['return'] = np.log(df['c'] / df['c'].shift(1))

    # 2) Lagged returns capture recent momentum
    for lag in lags:
        df[f'return_lag_{lag}'] = df['return'].shift(lag)

    # 3) Rolling stats capture trend & volatility
    for w in windows:
        df[f'return_roll_mean_{w}'] = df['return'].rolling(w).mean()
        df[f'return_roll_std_{w}']  = df['return'].rolling(w).std()

    df.dropna(inplace=True)
    return df

def create_labels(df, threshold=0):
    # Label = 1 if next-minute return > threshold, else 0
    y = (df['return'].shift(-1) > threshold).astype(int)
    # Align so that each row in X has a corresponding label in y
    return y.iloc[:-1], df.iloc[:-1]
