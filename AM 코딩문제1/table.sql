CREATE TABLE Users (
    userId INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100)
);

CREATE TABLE Trades (
    transactionId INT PRIMARY KEY,
    userId INT,
    symbol VARCHAR(10),
    type VARCHAR(4),
    price DECIMAL(10, 2),
    qty DECIMAL(10, 3),
    time TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES Users(userId)
);