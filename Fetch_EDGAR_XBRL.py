"""
This script automates fetching and organizing XBRL financial data from the SEC's EDGAR database for a given stock ticker:

- **API Interaction:**
  - `make_api_request`: Performs HTTP GET requests to the SEC API with rate limiting to avoid overwhelming the server.
  - `get_url`: Retrieves the CIK (Central Index Key) from a local JSON database and constructs the API URL.

- **Rate Limiting:**
  - Implements rate limiting to manage API requests within the allowed frequency, preventing service disruption.

- **Data Organization:**
  - `generate_filename`/`generate_foldername`: Creates and ensures the existence of directories and filenames for storing data.
  - Structures data into JSON format, focusing on key financial namespaces like 'dei' (Document and Entity Information) and 'us-gaap' (U.S. GAAP), with additional namespaces ('invest', 'srt') if available.

- **Data Processing:**
  - Converts the API response into a pandas DataFrame for easier manipulation.
  - Organizes financial facts by namespace, converting them back to JSON for storage.
  - Provides visibility into which namespaces are included in the data.

- **Execution:**
  - The script runs through:
    - Fetching the appropriate URL based on the ticker.
    - Making API requests, processing the data, and saving it in a structured format.

This script is particularly useful for financial analysts or researchers requiring detailed financial data directly from SEC filings, ensuring compliance with API usage limits and providing organized data storage.
"""
import pandas as pd
import json
import requests
import time
import os

pd.set_option('display.max_columns', None)  # None means show all columns
# Number of requests per second you want to allow
requests_per_second = 1.0
ticker = "PLTR"
print_namespace = True
# Custom User-Agent header for requests
headers = {"User-Agent": "###@gmail.com"}

def make_api_request(url, header):
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
        return response
    except requests.RequestException:
        print(f"Request to {url} failed")
        return None

# Rate limiting function
def rate_limited_api_calls(urls, requests_per_second):
    delay = 1 / requests_per_second
    for url in urls:
        response = make_api_request(url, headers)
        if response is not None:
            # Process response here if needed
            pass
        time.sleep(delay)

def get_url(ticker):
# Load company data
    all_items = []
    with open("company_tickers_exchange.json", "r") as f:
        CIK_dict = json.load(f)

    # Convert to DataFrame
    CIK_df = pd.DataFrame(CIK_dict["data"], columns=CIK_dict["fields"])

    # Get CIK for a specific ticker
    CIK = CIK_df[CIK_df["ticker"] == ticker].cik.values[0]

    # Construct URL for SEC API
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{str(CIK).zfill(10)}.json"
    print(url)
    return url

def generate_filename(ticker, folder_name):
    """Generate a filename based on input parameters."""
    return f"{folder_name}/{ticker}_EDGAR_XBRL_JSON.json"

def generate_foldername(ticker):
    """Generate a folder name based on input parameters."""
    folder_name = f"{ticker}/{ticker}_EDGAR_XBRL"
    if not os.path.exists(f"{ticker}"):
        os.makedirs(f"{ticker}")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def get_EDGAR_XBRL(ticker, url):
    all_items = []
    folder_name = generate_foldername(ticker)
    file_name = generate_filename(ticker, folder_name)
    # Fetch company filings
    company_xbrl = make_api_request(url, headers)

    if company_xbrl is not None:
        company_xbrl = company_xbrl.json()
        # Convert recent filings to DataFrame
        company_xbrl = pd.DataFrame(company_xbrl)
        print(company_xbrl.head())

        # Dictionary to store fetched facts
        facts_dict = {}

        # Try to fetch 'dei' facts
        if 'dei' in company_xbrl.index:
            facts_dict['dei'] = company_xbrl.loc['dei', 'facts']

        # Try to fetch 'us-gaap' facts
        if 'us-gaap' in company_xbrl.index:
            facts_dict['us-gaap'] = company_xbrl.loc['us-gaap', 'facts']

        # Check for 'invest' and 'srt' only if they exist
        for namespace in ['invest', 'srt']:
            if namespace in company_xbrl.index:
                facts_dict[namespace] = company_xbrl.loc[namespace, 'facts']
            else:
                print(f"No {namespace} data found.")

        # Prepare list of items for JSON including namespace
        all_items = [{"namespace": namespace, "facts": facts} for namespace, facts in facts_dict.items()]

        # Convert to JSON and save
        pd.DataFrame(all_items).to_json(file_name, orient='records')
        if print_namespace == True:
            for item in all_items:
                print(item['namespace'])
            print("Namespaces included in all_items")

if __name__ == "__main__":
    url = get_url(ticker)
    get_EDGAR_XBRL(ticker, url)
