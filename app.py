from flask import Flask, request
import json
import statsmodels.api as sm
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)


def get_forecast(year, month):
    forecast_date = str(year) + '-' + str(month) + '-' + '01'
    end_date = '2020-12-01'
    model = sm.load('forecast_model.pickle')
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
        return {'prediction': round(forecast, 2)}

    except (NameError, ValueError):
        return {'error': 'Invalid data'}
