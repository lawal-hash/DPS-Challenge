from flask import Flask, request
import json
from datetime import datetime
import statsmodels.api as sm
from util import load_data
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)


def fit_model():
    data_df = load_data('Alkoholunfälle_insgesamt.csv')
    arima_model = sm.tsa.arima.ARIMA(data_df['WERT'], seasonal_order=(5, 0, 6, 12), trend='c')
    time_series = arima_model.fit()
    return time_series


model = fit_model()
print(model)


def get_forecast(year, month):
    forecast_date = str(year) + '-' + str(month) + '-' + '01'
    end_date = '2020-12-01'
    forecast = model.predict(start=end_date, end=forecast_date)
    return forecast


@app.route('/forecast', methods=['POST'])
def forecast_accident():
    try:
        parsed = json.loads(request.data)
        print(parsed)
        year = parsed.get('year')
        month = parsed.get('month')

        if year is None or month is None:
            return {'error': 'expects year and month'}

        # @TODO
        forecast = get_forecast(year, month)
        print(forecast)
        forecast = forecast[-1]
        return {'prediction': round(forecast,2)}

    except (NameError, ValueError) as ex:
        return {'error': 'Invalid data'}
