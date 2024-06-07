import sqlite3

class ExchangeCredentials:
    def __init__(self):
        self.conn = sqlite3.connect('exchange_credentials.db')
        self.conn.row_factory = sqlite3.Row  # Row factory를 설정하여 Row 객체를 사용
        self.cursor = self.conn.cursor()
    
    def create_table(self):
        # 테이블 생성
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ExchangeCredentials (
            UserId INT PRIMARY KEY,
            Exchange VARCHAR(50),
            APIKey VARCHAR(100),
            SecretKey VARCHAR(100)
        )
        ''')

        # 데이터베이스 변경 사항 저장
        self.conn.commit()

    # 데이터 삽입 함수
    def insert_exchange_credential(self, user_id, exchange, api_key, secret_key):
        self.cursor.execute('''
        INSERT INTO ExchangeCredentials (UserId, Exchange, APIKey, SecretKey)
        VALUES (?, ?, ?, ?)
        ''', (user_id, exchange, api_key, secret_key))
        self.conn.commit()

    # 데이터 조회 함수
    def get_exchange_credentials(self):        
        self.cursor.execute('SELECT * FROM ExchangeCredentials')
        rows = self.cursor.fetchall()

        # 컬럼 이름과 함께 데이터를 출력
        result = []
        for row in rows:
            result.append(dict(row))

        return result

    # 데이터 삭제 함수
    def delete_exchange_credential(self, user_id):        
        # 특정 데이터를 삭제
        self.cursor.execute('''
        DELETE FROM ExchangeCredentials WHERE UserId = ?
        ''', (user_id,))
        
        self.conn.commit()
        
    # 커넥션 해제
    def close(self):
        self.conn.close()