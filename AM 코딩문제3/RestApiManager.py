import requests
import datetime as dt

class RestApiManager:
    def get_historical_data(self, api_url):
        response = requests.get(api_url)
        data = response.json()
        candles = []
        for item in data:
            candles.append({
                'time': dt.datetime.fromtimestamp(item[0] / 1000).strftime('%Y-%m-%d'),
                'open': float(item[1]),
                'high': float(item[2]),
                'low': float(item[3]),
                'close': float(item[4])
            })
        return candles