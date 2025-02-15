### Welcome to Market_Research_Experiments
I've created this suite of Python tools as part of my journey into the world of financial market research, specifically tailored to analyze stock market data. This project is both a demonstration of my skills and passion for data science in finance, aimed at showcasing my capabilities to potential employers. Here's what you'll find in this repository:

- Data Acquisition from SEC filings and the Alpha Vantage API, which I've used to gather real-world financial data for analysis.
- Data Parsing scripts that transform raw financial data into structured, analyzable formats, reflecting my attention to detail and ability to handle complex data structures.
- Exploratory Data Analysis (EDA) where I've utilized libraries like Plotly to visualize and interpret trends, correlations, and patterns, showcasing my ability to derive insights from data.

### Fetching
#### Data Acquisition and API Utilization:
##### SEC Filings (XBRL):
This module interacts with the SEC's EDGAR database to fetch the latest financial filings in XBRL format. 
Tools are included for:
- Automatically identifying and downloading specific filings using CIK numbers.
- Handling rate limits to ensure compliance with SEC's API usage policies.
- Parsing complex XBRL structures to extract relevant financial data.

##### Alpha Vantage API:
Utilizes Alpha Vantage's robust API to collect various financial data points:
- Financial Statements: Income statements, balance sheets, cash flow statements for in-depth company analysis.
- News Sentiment Analysis: Collects sentiment scores from news articles related to stocks to gauge market sentiment.
- Intraday Stock Data: Fetches high-frequency (5-minute intervals by default) OHLCV (Open, High, Low, Close, Volume) data for intraday market analysis.
- Includes scripts for managing API keys securely and handling API call quotas efficiently.

### Parsing
#### Data Transformation and Preprocessing:
##### XBRL Data Parsing:
- Converts the hierarchical and complex structure of XBRL data into more manageable pandas DataFrames or JSON formats.
- Implements error handling for missing or malformed data.
- Standardizes financial metrics across different filings to ensure consistency in analysis.

##### OHLCV Data Processing:
Parses JSON or CSV data into structured time series data, focusing on:
- Cleaning and aligning data for consistency, especially for stocks with differing reporting times.
- Handling missing data points, outliers, and ensuring time series integrity.

##### News Sentiment Data:
Processes raw sentiment data into a format suitable for correlation with stock movements, including:
- Time-stamping news events to match with stock price changes.
- Aggregating sentiment by time frames or sources for more nuanced analysis.

### EDA (Exploratory Data Analysis)
#### Data Visualization and Insight Generation:
##### Time Series Visualization:
Uses Plotly for interactive and dynamic visualizations:
- Plots stock price movements, volume, and volatility over time.
- Visualizes financial metrics like revenue, profit, or debt alongside stock performance.

##### Correlation and Pattern Recognition:
Leverages statistical methods to uncover relationships:
- Between stock returns and financial statements.
- Between news sentiment and stock price movements, including lag analysis to understand the impact timeline.


#### Note:
This repository works from a .env file of the following format:
- TICKER = 'XXXX'
- EMAIL = 'email@gmail.com'
- ALPHA_VANTAGE_API_KEY ='APIKEY'
- FRED_API_KEY = 'APIKEY'

