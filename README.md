📊 Azure Automated Crypto ETL & Power BI Pipeline
This is a comprehensive End-to-End Data Engineering project that automates the ingestion, storage, transformation, and professional visualization of real-time cryptocurrency data using the Microsoft Azure Ecosystem and Power BI.

🏗️ Architecture & Medallion Workflow
The project follows the Medallion Architecture to ensure data quality and separation of concerns:

Bronze (Raw): Unstructured JSON files from CoinGecko API stored in Azure Blob Storage.

Silver (Structured): Cleaned data moved from JSON to Azure SQL Database via Azure Data Factory.

Gold (Curated): Optimized SQL Views that provide only the latest market snapshots for high-performance reporting.

🛠️ Tech Stack
Source: CoinGecko API

Orchestration & Ingestion: Azure Logic Apps (Daily Trigger)

Data Lake (Bronze): Azure Blob Storage

ETL & Integration: Azure Data Factory (ADF)

Data Warehouse (Silver/Gold): Azure SQL Database

Visualization: Power BI Desktop & Power BI Service (Cloud)

🔄 Workflow Details
1. Ingestion (Bronze Layer)
Azure Logic Apps runs on a daily schedule.

It fetches data via HTTP GET and saves it to Blob Storage with a dynamic timestamp: crypto_@{utcNow()}.json.

2. ETL & Transformation (Silver Layer)
Azure Data Factory manages the move to SQL.

Copy Activity: Uses wildcard paths to process all daily JSON files.

Schema Mapping: Precisely maps nested JSON values to structured SQL columns (converting types to Double/Decimal for financial accuracy).

3. Data Modeling (Gold Layer)
To optimize the dashboard, we implemented a Gold View in SQL. Instead of loading millions of historical rows into the "Current Price" card, we use a view that calculates the latest state:

SQL
CREATE VIEW vw_gold_aktualne_ceny AS
SELECT name, price_usd, last_updated
FROM CryptoPrices
WHERE last_updated = (SELECT MAX(last_updated) FROM CryptoPrices);
4. Professional Visualization (Power BI)
The final dashboard provides actionable insights through:

Interactive Slicers: Tile-style buttons for seamless switching between Bitcoin, Ethereum, and Solana.

Advanced Formatting: Dark mode UI with Conditional Color Gradients on bar charts (highlighting top performers).

AI Integration: Smart Narrative summaries that automatically explain market trends in plain language.

DAX Custom Measures: Custom logic to handle currency formatting and avoid "Auto-scaling" issues (e.g., removing the "K" for thousands to show exact values).

🛠️ Problem Solving & Technical Challenges
🗓️ The ISO Date Challenge (Power Query)
The API provided timestamps in an ISO format (e.g., 2026-03-30T12:00:00Z) which caused errors in standard European locales.

Solution: Implemented a "Using Locale" transformation in Power Query, forcing the interpreter to use English (United States) for the last_updated column.


💰 Precision Formatting (DAX)
To ensure the dashboard displayed exact dollar values without forced rounding or "K" suffixes, I developed a custom DAX measure:

Útržok kódu
Cena Displej = FORMAT(SUM(vw_gold_aktualne_ceny[price_usd]), "#,##0.00 $")
🚀 End-to-End Automation
The entire pipeline is fully autonomous:

07:00 AM: Azure Logic Apps & ADF Trigger start the data flow.

07:15 AM: Data is cleaned and stored in Azure SQL.

08:00 AM: Power BI Cloud Scheduled Refresh triggers, pulling the new "Gold" data.

Result: The user wakes up to a fresh, updated dashboard without a single manual click.

<img width="1542" height="871" alt="Krypto Power Bi" src="https://github.com/user-attachments/assets/f1fc145c-cf58-4272-8064-8530da75fad1" />
