import pandas as pd
import statsmodels.api as sm
from numpy.linalg import LinAlgError
import warnings

warnings.filterwarnings("ignore")


def load_data(path):
    Alkoholunfalle_df = pd.read_csv(path, parse_dates=['MONAT'])
    Alkoholunfalle_df['MONAT'] = pd.to_datetime(Alkoholunfalle_df['MONAT'], errors='coerce', format='%Y%m')
    Alkoholunfalle_df = Alkoholunfalle_df.reindex(index=Alkoholunfalle_df.index[::-1])
    Alkoholunfalle_df.reset_index(inplace=True, drop=True)
    Alkoholunfalle_df = Alkoholunfalle_df.set_index(['MONAT'])
    Alkoholunfalle_df.sort_index(ascending=True, inplace=True)
    return Alkoholunfalle_df


# Split dataset into 80% train and 20% test

data_df = load_data('Alkoholunfälle_insgesamt.csv')
print(data_df.index)

row, col = data_df.shape
train_idx = int(0.8 * row)
df_train = data_df[:train_idx]
df_valid = data_df[train_idx:]

# Uni-variate Time Series Model
arima_model = sm.tsa.arima.ARIMA(data_df['WERT'], order=(1, 0, 10), trend='ct')
time_series = arima_model.fit()
# print(time_series.summary())


# Hyperparameter Tuning: Grid Search
# The parameters to be tune are order= (p, d, q) and trend = {‘n’,’c’,’t’,’ct’}

test_results = {}
trend = ['n', 'c', 't', 'ct']

for i in range(len(trend)):
    raise_error = 0
    counter = 0
    for p in range(10, 50, 5):
        for q in range(0, 50, 10):
            raise_error = 0
            try:
                arima_model = sm.tsa.arima.ARIMA(data_df['WERT'], order=(p, 0, q), trend=trend[i])
                time_series = arima_model.fit()
            except ValueError:
                raise_error += 1
            except LinAlgError:
                raise_error += 1
            finally:
                test_results[(p, q, trend[i])] = [time_series.bic, time_series.aic, raise_error]
                counter += 1
                print(counter)

test_results_df = pd.DataFrame(test_results).T
test_results_df.to_csv('hyperparameter_tuning.csv')

# df = pd.read_csv("").T
# print(df.head())
