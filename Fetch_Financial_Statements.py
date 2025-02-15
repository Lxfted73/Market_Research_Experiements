"""
This script interacts with the Alpha Vantage API to fetch financial statements for a specified stock symbol.
It performs the following operations:

- **API Interaction:**
  - Defines functions for querying different financial statements (Income Statement, Balance Sheet, Cash Flow, Earnings).
  - Generates URLs for API requests for each financial statement type.

- **File and Folder Management:**
  - Creates unique filenames for each statement based on the symbol and statement type.
  - Organizes data into a structured folder system under the symbol's name.

- **Data Retrieval and Storage:**
  - Fetches financial data for each statement type.
  - Saves the retrieved data in JSON format within the designated folder.

- **Execution Flow:**
  - Iterates through a list of financial statement types for a given symbol.
  - Ensures a directory structure exists or creates it if it doesn't.
  - Requests data, saves it, and confirms the file save operation.

The script uses a predefined API key and focuses on one symbol ('PLTR') but can be expanded for multiple symbols.
"""


import json
import os
import requests
from dotenv import load_dotenv

function_income_statement = 'INCOME_STATEMENT'
function_balance_sheet = 'BALANCE_SHEET'
function_cash_flow = 'CASH_FLOW'
function_earnings = 'EARNINGS'
function_list = [function_income_statement, function_balance_sheet,function_cash_flow, function_earnings]

load_dotenv()
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
print_dotenv = True
symbol = os.getenv("TICKER")
symbol_list = [symbol]

if print_dotenv == True:
    # Use them in your code
    if api_key:
        print(f"API KEY loaded: {api_key}")
    else:
        print("API KEY not found in .env!")
    if symbol:
        print(f'TICKER/SYMBOL loaded: {symbol}')
    else:
        print("TICKER/SYMBOL not found in .env!")


def generate_statement_url(function, symbol, api_key):
    # Base URL for the API
    base_url = 'https://www.alphavantage.co/query?'

    # Construct query parameters
    params = {
        'function': function,
        'symbol': symbol,
        'apikey': api_key  # Assuming api_key is defined elsewhere
    }

    # Manually construct the query string to match the exact format
    query_string = f"function={params['function']}&symbol={params['symbol']}&apikey={params['apikey']}"

    # Combine base URL with query string
    url = f"{base_url}{query_string}"

    return url

def generate_filename(symbol, function):
    # Cleaning up the ticker string by removing commas and replacing with underscores
    clean_symbol = symbol.replace(',', '_').replace(':', '_')

    # Constructing the filename
    filename = f"{clean_symbol}_{function}.json"

    return filename

def generate_folder_name(ticker):
    clean_ticker = ticker.replace(',', '_').replace(':', '_')
    folder_name = f"{clean_ticker}/{clean_ticker}_FINANCIAL_STATEMENTS"
    return folder_name


def request_url(url_input, file_name):
    url = url_input
    r = requests.get(url)
    json_data = r.json()
    with open(file_name, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)  # indent=4 for pretty printing
    print(f"Json File saved as:{file_name}")

for symbol in symbol_list:
    folder_name = generate_folder_name(symbol)
    for statement in function_list:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        url = generate_statement_url(statement, symbol,api_key)
        print(url)
        file_name = generate_filename(symbol, statement)
        destination_file_path = os.path.join(folder_name, file_name)
        request_url(url, destination_file_path)




