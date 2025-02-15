"""
This script interfaces with the Alpha Vantage API to gather news sentiment data for a specified stock ticker:

- **Data Fetching:** Queries the API for news sentiment across multiple topics within a given time frame.
- **URL Generation:** Constructs specific API request URLs with parameters like function, ticker, time, topics, and API key.
- **File Management:**
  - Generates unique filenames for data storage.
  - Creates a structured folder system to organize the JSON files by ticker and time range.
- **Data Storage:**
  - Fetches data via HTTP requests.
  - Checks for the presence of data in the API response.
  - Saves valid responses as JSON files.

The script iterates through a predefined list of topics to collect and store comprehensive sentiment data.
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
print_dotenv = True
ticker = os.getenv("TICKER")


if print_dotenv == True:
    # Use them in your code
    if ticker:
        print(f" loaded: {ticker}")
    else:
        print("API KEY not found in .env!")

def generate_articles_url(function, ticker, time_from, time_to, topics, limit, api_key):
    # Base URL for the API
    base_url = 'https://www.alphavantage.co/query?'

    # Construct query parameters
    params = {
        'function': function,
        'tickers': ticker,
        'time_from': time_from,
        'time_to': time_to,
        'limit': limit,
        'topics': topics,
        'apikey': api_key  # Assuming api_key is defined elsewhere
    }

    # Manually construct the query string to match the exact format
    query_string = f"function={params['function']}&tickers={params['tickers']}&time_from={params['time_from']}&time_to={params['time_to']}&limit={params['limit']}&topics={params['topics']}&apikey={params['apikey']}"

    # Combine base URL with query string
    url = f"{base_url}{query_string}"

    return url


def generate_filename(ticker, time_from, time_to, function, limit, topics):
    # Cleaning up the ticker string by removing commas and replacing with underscores
    clean_ticker = ticker.replace(',', '_').replace(':', '_')

    # Constructing the filename
    filename = f"{clean_ticker}_{function}_{time_from}_to_{time_to}_limit{limit}_topic{topics}.json"

    return filename

def generate_folder_name(ticker, time_from, time_to, function):
    clean_ticker = ticker.replace(',', '_').replace(':', '_')
    folder_name = f"{clean_ticker}/{clean_ticker}_{function}_{time_from}_to_{time_to}"
    return folder_name



def request_url(url_input, file_name):
    url = url_input
    r = requests.get(url)
    json_data = r.json()
    if json_data['items'] == '0':
        print(f"{url}\n has 0 items")
        return
    else:
        with open(file_name, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)  # indent=4 for pretty printing
        print(f"Json File saved as:{file_name}")




# Example usage:
# Assuming api_key is defined before this point
ticker = 'PLTR'  # CRYPTO:BTC,CRYPTO:SOL,CRYPTO: ETH'
time_from = '20240101T0000'  # YYYYMMDDTHHMM 20240110T0130
time_to = '20250130T0000'
function = 'NEWS_SENTIMENT'
limit = 1000
topics = 'technology' # Example topics
topic_list = ['blockchain', 'earnings', 'ipo', 'mergers_and_acquisitions',
              'financial_markets', 'economy_fiscal', 'economy_monetary', 'economy_macro', 'energy_transportation',
              'finance', 'life_sciences', 'manufacturing', 'real_estate', 'retail_wholesale', 'technology']


# url = generate_articles_url(function, ticker, time_from, topics, limit, api_key)
# file_name = generate_filename(function, ticker, time_from, limit, topics)
# request_url(url, file_name)

folder_name = generate_folder_name(ticker, time_from, time_to, function)

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

for topic in topic_list:
    url = generate_articles_url(function, ticker, time_from, time_to, topic, limit, api_key)
    print(url)
    file_name = generate_filename(ticker, time_from, time_to,function, limit, topic)
    destination_file_path = os.path.join(folder_name, file_name)
    request_url(url, destination_file_path)
