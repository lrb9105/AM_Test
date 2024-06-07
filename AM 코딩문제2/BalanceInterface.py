from abc import ABC, abstractmethod

class BalanceInterface(ABC):
    # signature 생성
    @abstractmethod
    def create_signature(self, *args, **kwargs) -> str:
        pass

    # 자산 조회
    @abstractmethod
    def get_balance(self, api_key: str, secret_key: str) -> any:
        pass

    # 자산데이터 정규화
    @abstractmethod
    def normalize_balance(self, balance_data: dict) -> dict:
        pass