import json
from flask import Flask, render_template
import threading
from RestApiManager import RestApiManager
from SocketManager import SocketManager

app = Flask(__name__)
restApiManager = RestApiManager()
socketManager = SocketManager(app)

# Binance API URLs
spot_api_url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d"
future_api_url = "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1d"

# Binance WebSocket URLs
spot_socket = "wss://stream.binance.com:9443/ws/btcusdt@kline_1d"
future_socket = "wss://fstream.binance.com/ws/btcusdt@kline_1d"

@app.route('/')
def index():
    initial_spot_data = restApiManager.get_historical_data(spot_api_url)
    initial_future_data = restApiManager.get_historical_data(future_api_url)
    return render_template('index.html', initial_spot_data=json.dumps(initial_spot_data), initial_future_data=json.dumps(initial_future_data))

if __name__ == '__main__':
    spot_thread = threading.Thread(target=socketManager.start_ws, args=(spot_socket, 'spot'))
    future_thread = threading.Thread(target=socketManager.start_ws, args=(future_socket, 'future'))
    spot_thread.start()
    future_thread.start()
    socketManager.start()
