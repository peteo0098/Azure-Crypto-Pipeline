Azure Automated Crypto ETL Pipeline 

This is an end-to-end data engineering project that automates the ingestion, storage, and transformation of real-time cryptocurrency data using **Microsoft Azure**.

Project Overview
The aim of this project is to develop a scalable, cloud-native pipeline to monitor market data for major cryptocurrencies. The system automatically retrieves data from an external API, stores it in a raw format (Data Lake), and converts it into a structured SQL database for analysis.

Tech Stack
- **Source:** [CoinGecko API](https://www.coingecko.com/en/api)
- **Orchestration & Ingestion:** Azure Logic Apps
- **Data Lake (Bronze Layer):** Azure Blob Storage
- **ETL & Data Integration:** Azure Data Factory (ADF)
- **Data Warehouse (Gold Layer):** Azure SQL Database

Architecture & Workflow

1. Ingestion (Bronze Layer)
* **Azure Logic Apps** is set up with a trigger that recurs daily.
* It makes an HTTP GET request to the CoinGecko API.
* The raw JSON response is stored directly into **Azure Blob Storage** with a dynamic timestamp: `crypto_@{utcNow()}.json`.

2. Transformation & Loading (Gold Layer)
* **Azure Data Factory** manages the transfer of data from Blob storage to the SQL database.
* **Copy Activity:** Utilizes a wildcard file path (`*.json`) to select all ingested files.
* **Schema Mapping:** Converts nested JSON fields (id, symbol, current_price, market_cap, last_updated) into structured columns in the SQL table.

3. Storage & Analysis
* The data is stored in an **Azure SQL Database** (Basic Tier).
* A predefined schema guarantees data integrity and facilitates relational queries.

SQL Schema
```sql
CREATE TABLE CryptoPrices (
RecordID INT IDENTITY(1,1) PRIMARY KEY,
CryptoID VARCHAR(50) NOT NULL,
Symbol VARCHAR(10) NOT NULL,
PriceUSD DECIMAL(18,2) NOT NULL,
MarketCap BIGINT,
LastUpdated DATETIME2,
IngestionTime DATETIME2 DEFAULT GETDATE()
);
