import pandas as pd
import numpy as np
import statsmodels.api as sm
from numpy.linalg import LinAlgError
import warnings

warnings.filterwarnings("ignore")

Alkoholunfalle_df = pd.read_csv('Alkoholunfälle_insgesamt.csv', parse_dates=['MONAT'])
Alkoholunfalle_df = Alkoholunfalle_df.reindex(index=Alkoholunfalle_df.index[::-1])
Alkoholunfalle_df.reset_index(inplace=True, drop=True)
Alkoholunfalle_df = Alkoholunfalle_df.set_index(['MONAT'])
print(Alkoholunfalle_df.head())




# Split dataset into 80% train and 20% test
row, col = Alkoholunfalle_df.shape
train_idx = int(0.8* row)
df_train = Alkoholunfalle_df[:train_idx]
df_valid = Alkoholunfalle_df[train_idx:]


# Time Series Model
arima_model  = sm.tsa.arima.ARIMA(Alkoholunfalle_df['WERT'], order=(1,0,1), trend='ct')
time_series = arima_model.fit()
print(time_series.summary())