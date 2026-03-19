CREATE TABLE CryptoPrices (
    RecordID INT IDENTITY(1,1) PRIMARY KEY,
    CryptoID VARCHAR(50),
    Symbol VARCHAR(10),
    PriceUSD DECIMAL(18,2),
    MarketCap BIGINT,
    LastUpdated DATETIME2,
    IngestionTime DATETIME2 DEFAULT GETDATE()
);