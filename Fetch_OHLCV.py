"""
This script automates the retrieval of intraday stock data from the Alpha Vantage API for a specific symbol across all months of a given year:

- **API Interaction:**
  - `generate_url`: Constructs API request URLs with parameters like symbol, interval, and specific month.
  - Fetches data for each month using the Alpha Vantage API.

- **Data Organization:**
  - `generate_filename`: Creates unique filenames to store data for each month.
  - `generate_foldername`: Establishes a directory structure to categorize data by year and symbol.

- **Data Storage:**
  - `request_url`: Performs HTTP requests to fetch data and saves it in JSON format within the created directory.

- **Date Handling:**
  - `generate_months`: Generates a list of months in 'YYYY-MM' format for the specified year, ensuring comprehensive coverage of the year's data.

- **Execution:**
  - `main`: Orchestrates the process by:
    - Creating a list of months to process.
    - Ensuring directory structure exists.
    - Iterating through each month, generating URLs, fetching, and saving data accordingly.

This script is tailored for financial analysts or researchers needing detailed, time-series intraday stock data, automating the collection process for ease and consistency in data gathering.
"""

import requests
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
print_dotenv = True
symbol = os.getenv("TICKER")
symbol_list = [symbol]
# API key should be set before running the script
interval = '5min'
function = 'TIME_SERIES_INTRADAY'
adjusted = 'false'
extended_hours = 'true'
year = 2023
outputsize = 'full'

def generate_url(function, symbol, interval, month, outputsize, apikey):
    """Generate the URL for the Alpha Vantage API request."""
    base_url = 'https://www.alphavantage.co/query?'
    params = {
        'function': function,
        'symbol': symbol,
        'interval': interval,
        'month': month,
        'outputsize': outputsize,
        'apikey': apikey
    }
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    return f"{base_url}{query_string}"

def generate_filename(symbol, function, interval, month, outputsize):
    """Generate a filename based on input parameters."""
    return f"{symbol}_{function}_{interval}_month{month}_size{outputsize}.json"

def generate_foldername(symbol, function, interval, outputsize):
    """Generate a folder name based on input parameters."""
    if not os.path.exists(symbol):
        os.makedirs(symbol)
    return f"{symbol}/{symbol}_{function}_{interval}_year{outputsize}"

def request_url(url, file_name):
    """Fetch data from the given URL and save it to a JSON file."""
    response = requests.get(url)
    json_data = response.json()
    with open(file_name, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    print(f"JSON file saved as: {file_name}")

def generate_months(start_year):
    """Generate a list of months for a given year in 'YYYY-MM' format."""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(start_year + 1, 1, 1)
    months = []
    current_date = start_date
    while current_date < end_date:
        months.append(current_date.strftime('%Y-%m'))
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)
    return months

def main():
    months = generate_months(year)
    print(months)

    foldername = generate_foldername(symbol, function, interval, outputsize)
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    for month in months:
        url = generate_url(function, symbol, interval, month, outputsize, api_key)
        print(url)
        file_name = generate_filename(symbol, function, interval, month, outputsize)
        destination_file_path = os.path.join(foldername, file_name)
        request_url(url, destination_file_path)

if __name__ == "__main__":
    main()