import websocket
import json
import datetime as dt
from flask_socketio import SocketIO

class SocketManager:
    def __init__(self, app):
        self.socketio = SocketIO(app)
        self.app = app
        
    def on_message(self, ws, message, market):
        json_message = json.loads(message)
        kline = json_message['k']
        
        candle = {
                'time': dt.datetime.fromtimestamp(kline['t'] / 1000).strftime('%Y-%m-%d'),
                'open': float(kline['o']),
                'high': float(kline['h']),
                'low': float(kline['l']),
                'close': float(kline['c']),
            }
        
        if market == 'spot':
            self.socketio.emit('spot_data', candle)
        elif market == 'future':
            self.socketio.emit('future_data', candle)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        print("### opened ###")
        
    def start_ws(self, socket, market):
        ws = websocket.WebSocketApp(socket, 
                                on_open=self.on_open, 
                                on_message=lambda ws, msg: self.on_message(ws, msg, market), 
                                on_error=self.on_error, 
                                on_close=self.on_close)
        ws.run_forever()   
    
    def start(self):
        self.socketio.run(self.app, port=8000)