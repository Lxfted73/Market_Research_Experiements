"""
This script processes XBRL financial data from EDGAR filings for a specified stock ticker:

- **Data Loading:**
  - Reads JSON data from a file path specific to the ticker's EDGAR XBRL filings.
  - Handles both dictionary and list JSON formats for flexibility.

- **Data Conversion:**
  - `make_df`: Converts JSON data into a pandas DataFrame, adjusting for different data structures.
  - Handles errors like file not found or JSON decoding issues.

- **Date Processing:**
  - `to_datetime`: Converts date fields in nested dictionaries to pandas datetime objects for consistency.

- **Namespace Parsing:**
  - `parse_namespace`: Extracts and organizes financial facts by namespace (e.g., 'dei', 'us-gaap') and fact type.
  - Processes data units and handles structural inconsistencies.

- **Comprehensive Parsing:**
  - `parse_EDGAR_XBRL_all`: Orchestrates parsing across predefined namespaces, creating a nested dictionary of financial facts.
  - Ensures all relevant data is captured and structured.

- **Execution:**
  - When run directly, processes data for the specified ticker ('PLTR'), with optional JSON output for debugging.

This script is ideal for financial analysts or researchers needing to extract and structure detailed financial data from EDGAR filings for analysis, ensuring robust error handling and data consistency.
"""

import pandas as pd
import json
import os

ticker = "PLTR"
pd.set_option('display.max_columns', None)


def make_df(ticker):
    path = f"{ticker}/{ticker}_EDGAR_XBRL/{ticker}_EDGAR_XBRL_JSON.json"
    try:
        with open(path, 'r') as file:
            data = json.load(file)
        if isinstance(data, dict):  # If data is already a dictionary
            return pd.DataFrame.from_dict(data, orient='index')
        elif isinstance(data, list):  # If data is a list of dictionaries or other elements
            # Here we assume each element in the list represents a different namespace or fact
            # You might need to adjust this based on your actual JSON structure
            df_data = {item['namespace']: item for item in data if 'namespace' in item}
            return pd.DataFrame.from_dict(df_data, orient='index')
        else:
            raise ValueError("Unexpected data format")
    except FileNotFoundError:
        print(f"File not found for ticker: {ticker}")
        return None
    except json.JSONDecodeError:
        print(f"JSON decoding error for ticker: {ticker}")
        return None


def to_datetime(dict_data):
    for key, value in dict_data.items():
        if isinstance(value, dict) and 'filed' in value:
            dict_data[key]['filed'] = pd.to_datetime(value['filed'])


def parse_namespace(df, namespace):
    try:
        # Assuming 'facts' is a direct attribute under each namespace
        facts = df.loc[namespace]['facts']
        result_dict = {}
        for fact_type, fact_details in facts.items():
            key = f"{namespace}_{fact_type}"
            try:
                units = fact_details.get('units', {})
                for unit_type, data in units.items():
                    for dict_item in data:
                        to_datetime(dict_item)
                    result_dict[f"{key}_{unit_type}"] = data
            except AttributeError:
                print(f"Fact '{fact_type}' does not have expected structure")
        return result_dict
    except KeyError:
        print(f"Namespace '{namespace}' not found in the dataframe")
        return {}


def parse_EDGAR_XBRL_all(ticker):
    df = make_df(ticker)
    if df is None:
        return {}

    all_dict = {}
    for namespace in ['dei', 'invest', 'us-gaap', 'srt']:
        all_dict[namespace] = parse_namespace(df, namespace)

    return all_dict


if __name__ == "__main__":
    data = parse_EDGAR_XBRL_all(ticker)
    # print(json.dumps(data, indent=2))  # Print formatted JSON for debugging