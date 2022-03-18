from flask import Flask, request
import json
from datetime import datetime
import statsmodels.api as sm
from model import load_data


def get_forecast(year, month):
    forcast_date = str(year) + '-' + str(month) + '-' + '01'
    end_date = '2020-12-01'
    data_df = load_data('Alkoholunfälle_insgesamt.csv')
    datetime_forcast_date = datetime.strptime(forcast_date, '%Y-%m-%d')
    datetime_end_date = datetime.strptime(end_date, '%Y-%m-%d')
    time_delta = (datetime_forcast_date.year - datetime_end_date.year) * 12 + (
                datetime_forcast_date.month - datetime_end_date.month)
    arima_model = sm.tsa.arima.ARIMA(data_df['WERT'], order=(49, 0, 10), trend='ct')
    time_series = arima_model.fit()
    forecast = time_series.forecast(time_delta)
    return forecast[-1]


app = Flask(__name__)


def get_prediction(year, month):
    return year + month


@app.route('/')
def welcome():
    return "<p>Hello, World!</p>"


@app.route('/forecast', methods=['POST'])
def forecast_accident():
    # data = request.data
    print(request.data)
    try:
        parsed = json.loads(request.data)
        print(parsed)
        year = parsed.get('year')
        month = parsed.get('month')

        if year is None or month is None:
            return {'error': 'expects year and month'}

        # @TODO
        forecast = get_forecast(year, month)
        return {'prediction': forecast}

    except Exception:
        return {'error': 'invalid data'}
