import pandas as pd
import statsmodels.api as sm
from numpy.linalg import LinAlgError
import warnings
from sklearn.metrics import mean_squared_error
from util import load_data

warnings.filterwarnings("ignore")

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

raise_error = 0
counter = 0
for i in range(len(trend)):
    for p in range(0, 10):
        for q in range(0, 10, 2):
            raise_error = 0
            try:
                arima_model = sm.tsa.arima.ARIMA(df_train['WERT'], seasonal_order=(p, 0, q, 12), trend=trend[i])
                time_series = arima_model.fit()
                y_pred = time_series.forecast(48)
                test_error = mean_squared_error(df_valid['WERT'], y_pred)
            except ValueError:
                raise_error += 1
            except LinAlgError:
                raise_error += 1
            finally:
                test_results[(p, q, trend[i])] = [test_error]
                counter += 1
                print(counter)

test_results_df = pd.DataFrame(test_results).T
test_results_df.to_csv('hyperparameter_tuning.csv')

# Selecting the best model parameters
# Model with the least test error


hyper_df = pd.read_csv('hyperparameter_tuning.csv')
hyper_df.rename(columns={"Unnamed: 0": "p", "Unnamed: 1": "q", 'Unnamed: 2': 'trend', '0': 'test_error'}, inplace=True)
best_param = hyper_df[hyper_df['test_error'] == hyper_df['test_error'].min()]
best_param.to_csv('best_model_parameter.csv', index=False)
