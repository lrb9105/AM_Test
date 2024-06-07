import requests
import hashlib
import hmac
import time
from urllib.parse import urlencode
from BalanceInterface import BalanceInterface

class BybitBalanceManager(BalanceInterface):
    # signature 생성
    def create_signature(self, api_key, secret_key, timestamp, params) -> str:
        param_str = f"{timestamp}{api_key}{urlencode(params)}"
        return hmac.new(secret_key.encode('utf-8'), param_str.encode('utf-8'), hashlib.sha256).hexdigest()

    # 자산 조회
    def get_balance(self, api_key, secret_key) -> any:
        url = "https://api-testnet.bybit.com/v5/account/wallet-balance"
    
        timestamp = int(time.time() * 1000)
        
        params = {"accountType": "UNIFIED"}
        
        sign = self.create_signature(api_key, secret_key, timestamp, params)
        
        headers = {
            'X-BAPI-SIGN': sign,
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-TIMESTAMP':  f"{timestamp}",

        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return self.normalize_balance(response.json())
        else:
            return {"error": response.text}

    # 자산 데이터 정규화
    def normalize_balance(self, balance_data) -> dict:
        normalized_data = {}
        for item in balance_data['result']['list'][0]['coin']:
            normalized_data[item['coin']] = float(item['walletBalance'])
            
        return normalized_data
    