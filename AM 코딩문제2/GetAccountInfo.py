from ExchangeCredentials import ExchangeCredentials
from OKXBalanceManager import OKXBalanceManager
from BinanceBalanceManager import BinanceBalanceManager
from BybitBalanceManager import BybitBalanceManager

OKXBalanceManager = OKXBalanceManager()
BinanceBalanceManager = BinanceBalanceManager()
BybitBalanceManager = BybitBalanceManager()
ExchangeCredentials = ExchangeCredentials()

def get_user_balance(credential):    
    balance_info = {}
    user_id = credential['UserId']
    exchange = credential['Exchange']
    api_key = credential['APIKey']
    secret_key = credential['SecretKey']
    
    if exchange == 'OKX':
        normalized_balance_data = OKXBalanceManager.get_balance(api_key, secret_key)
    elif exchange == 'Binance':
        normalized_balance_data = BinanceBalanceManager.get_balance(api_key, secret_key)
    elif exchange == 'Bybit':
        normalized_balance_data = BybitBalanceManager.get_balance(api_key, secret_key)
    
    balance_info[f"{user_id}" + "_" + exchange] = normalized_balance_data
    
    return balance_info

if __name__ == '__main__':
    # 데이터 조회
    credentials = ExchangeCredentials.get_exchange_credentials()
    
    # 자산 조회
    for credential in credentials:
        balance_info = get_user_balance(credential)
        print(balance_info)
        
    ExchangeCredentials.close()
        