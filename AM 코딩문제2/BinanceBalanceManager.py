import requests
import hashlib
import hmac
import time
from BalanceInterface import BalanceInterface

class BinanceBalanceManager(BalanceInterface):
    # signature 생성
    def create_signature(self, timestamp, secret_key) -> str:
        query_string = f"timestamp={timestamp}"
        return hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    # 자산 조회
    def get_balance(self, api_key, secret_key) -> any:
        url = "https://testnet.binance.vision/api/v3/account"
        timestamp = int(time.time() * 1000)
        signature = self.create_signature(timestamp, secret_key)
        headers = {
            "X-MBX-APIKEY": api_key,
            "Content-Type": "application/json"
        }
        params = {
            "timestamp": timestamp,
            "signature": signature
        }
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return self.normalize_balance(response.json())
        else:
            return {"error": response.text}

    def normalize_balance(self, balance_data) -> dict:
        normalized_data = {}
        for item in balance_data['balances']:
            normalized_data[item['asset']] = float(item['free'])
            
        # 잔액을 두 자리 소수로 포맷팅
        return normalized_data