"""
This script is designed to process OHLCV (Open, High, Low, Close, Volume) stock data from JSON files within a specified folder:

- **JSON Loading:**
  - `load_json`: Reads JSON content from a file path.

- **Data Parsing:**
  - `parse_ohlcv_data`: Converts JSON data specifically formatted for 5-minute interval OHLCV into a pandas DataFrame:
    - Extracts data under 'Time Series (5min)' key.
    - Converts numeric data types for consistency.
    - Renames 'index' to 'datetime' and converts to datetime format for time-based operations.

- **Folder Processing:**
  - `parse_ohlcv_folder`:
    - Iterates through all JSON files in the given folder.
    - Parses each file, handling potential errors or missing data.
    - Combines all valid DataFrames into one, sorting by datetime for chronological order.

- **Execution:**
  - When run directly, it processes all JSON files in a predefined folder, displaying the first few rows of the resulting DataFrame for verification.

This tool is particularly useful for financial data analysts or traders who need to aggregate and prepare high-frequency stock data for analysis or visualization, ensuring data consistency and readiness for time-series analysis.
"""

import pandas as pd
import os
import json

def load_json(file_path):
    """Load JSON data from the given file path."""
    with open(file_path, 'r') as f:
        return json.load(f)

def parse_ohlcv_data(ohlcv_data):
    """Parse OHLCV data from a dictionary into a pandas DataFrame."""
    if 'Time Series (5min)' in ohlcv_data:
        df = pd.DataFrame.from_dict(ohlcv_data['Time Series (5min)'], orient='index')
        columns = ['1. open', '2. high', '3. low', '4. close', '5. volume']
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col])

        df = df.reset_index()
        df = df.rename(columns={'index': 'datetime'})
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
    else:
        print(f"No 'Time Series (5min)' data in this file.")
        return None

def parse_ohlcv_folder(folder_path):
    """Parse all OHLCV JSON files in a folder, combining them into one DataFrame."""
    all_data = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        ohlcv_data = load_json(file_path)
        parsed_data = parse_ohlcv_data(ohlcv_data)
        if parsed_data is not None:
            all_data.append(parsed_data)
        else:
            print(f"Skipped file: {filename}")

    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        combined_data = combined_data.sort_values('datetime')
        return combined_data
    else:
        print("No valid OHLCV data found in the folder.")
        return None

if __name__ == "__main__":
    folder_path = 'TSM_TIME_SERIES_INTRADAY_5min_adjustedfalse_extendedtrue_year2024'
    result = parse_ohlcv_folder(folder_path)
    if result is not None:
        print(result.head())  # Display first few rows to check data