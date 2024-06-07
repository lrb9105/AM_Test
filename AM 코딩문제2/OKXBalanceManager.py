import requests
import hashlib
import hmac
import base64
from datetime import datetime
from BalanceInterface import BalanceInterface

class OKXBalanceManager(BalanceInterface):
    # signature 생성
    def create_signature(self, timestamp, method, request_path, secret_key, body="") -> str:
        prehash_string = f"{timestamp}{method}{request_path}{body}"
        signature = hmac.new(secret_key.encode('utf-8'), prehash_string.encode('utf-8'), hashlib.sha256).digest()
        return base64.b64encode(signature).decode()

    # 자산 조회
    def get_balance(self, api_key, secret_key) -> any:
        passphrase = "@amtest123Okx"
        url = "https://www.okx.com/api/v5/account/balance"
        
        timestamp = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
        method = "GET"
        request_path = "/api/v5/account/balance"
        signature = self.create_signature(timestamp, method, request_path, secret_key)
        
        headers = {
            "OK-ACCESS-SIGN": signature,
            "OK-ACCESS-KEY": api_key,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": passphrase,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return self.normalize_balance(response.json())
        else:
            return {"error": response.text}

    # 자산 데이터 정규화
    def normalize_balance(self, balance_data) -> dict:
        normalized_data = {}
        for item in balance_data['data'][0]['details']:
            normalized_data[item['ccy']] = float(item['availBal'])

        return normalized_data