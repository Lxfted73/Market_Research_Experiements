"""
This script automates the retrieval and organization of SEC filings for a specified company, focusing on XBRL filings:

- **Data Loading:**
  - `load_company_data`: Loads company information from a JSON file to map tickers to CIK numbers.

- **API Interaction:**
  - `make_api_request`: Manages HTTP requests to SEC APIs with custom headers for identification.
  - `fetch_XBRL`: Retrieves a list of filings with XBRL attachments from the SEC for the specified company.

- **Rate Limiting:**
  - `rate_limited_api_calls`: Implements a rate limit on API requests to comply with usage policies.

- **Filing Processing:**
  - `process_filing`: Downloads the HTML content of individual filings, saving them in a structured directory under the company's ticker name.
  - Focuses on the first 20 filings to prevent excessive API calls, but this limit can be adjusted.

- **Main Execution:**
  - `main`: Orchestrates the process by:
    - Fetching company and filing data.
    - Iterating through recent XBRL filings to download and save.

- **Customization:**
  - Tailored for 'PLTR' (Palantir Technologies) but easily adaptable for other tickers by changing the `ticker` variable.
  - Defaults to '10-K' forms but can be set to retrieve other form types.

This script is ideal for financial analysts or researchers needing direct access to SEC filings for detailed analysis or compliance checks, ensuring data is organized and accessible.
"""

import pandas as pd
import json
import requests
import time
import os

email = "###@gmail.com"
ticker = "PLTR"
form = "10-K"


pd.set_option("display.max_columns",  None)
pd.set_option("display.max_rows",  None)

# Custom User-Agent header for requests
headers = {"User-Agent": email}


def make_api_request(url):
    """
    Makes an API request and handles exceptions.

    :param url: URL to request
    :return: Response object or None if request fails
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException:
        print(f"Request to {url} failed")
        return None


def rate_limited_api_calls(urls, requests_per_second):
    """
    Executes API calls with rate limiting.

    :param urls: List of URLs to request
    :param requests_per_second: Rate limit in requests per second
    """
    delay = 1 / requests_per_second
    for url in urls:
        response = make_api_request(url)
        if response is not None:
            # Process response here if needed
            pass
        time.sleep(delay)


def load_company_data():
    """
    Loads company data from JSON file into a DataFrame.

    :return: DataFrame with company information
    """
    with open("company_tickers_exchange.json", "r") as f:
        CIK_dict = json.load(f)
    return pd.DataFrame(CIK_dict["data"], columns=CIK_dict["fields"])


def fetch_filings(CIK, ticker, form):
    """
    Fetches company filings from SEC API.

    :param CIK: Company's CIK number
    :param ticker: Company ticker symbol
    :param form: Form type to look for (e.g., '10-K')
    :return: DataFrame with relevant filings
    """
    url = f"https://data.sec.gov/submissions/CIK{str(CIK).zfill(10)}.json"
    print(url)

    response = make_api_request(url)
    if response is not None:
        company_filings = response.json()
        company_filings_df = pd.DataFrame(company_filings["filings"]["recent"])
        form_filings = company_filings_df[company_filings_df.form == form]
        return form_filings
    return pd.DataFrame()  # Return an empty DataFrame if no data was fetched

def fetch_XBRL(CIK, ticker):
    """
    Fetches company filings from SEC API.

    :param CIK: Company's CIK number
    :param ticker: Company ticker symbol
    :param form: Form type to look for (e.g., '10-K')
    :return: DataFrame with relevant filings
    """
    url = f"https://data.sec.gov/submissions/CIK{str(CIK).zfill(10)}.json"
    print(url)

    response = make_api_request(url)
    if response is not None:
        company_filings = response.json()
        company_filings_df = pd.DataFrame(company_filings["filings"]["recent"])
        xbrl_filing = company_filings_df[company_filings_df.isXBRL == 1]
        return xbrl_filing
    return pd.DataFrame()

def process_filing(ticker, CIK, row):
    """
    Processes individual filing by downloading and saving HTML.

    :param ticker: Company ticker symbol
    :param CIK: Company's CIK number
    :param row: DataFrame row containing filing details
    """
    access_number = row['accessionNumber'].replace("-", "")
    file_name = row['primaryDocument']

    filing_url = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{access_number}/{file_name}"
    print(filing_url)

    response = make_api_request(filing_url)
    if response is not None:
        directory = f"{ticker}_EDGAR_HTM/"
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory '{directory}' created successfully.")
        else:
            print(f"Directory '{directory}' already exists.")

        with open(f'{directory}/{file_name}', "w", encoding="utf-8") as f:
            f.write(response.text)


def main(ticker, form, requests_per_second=1.0):
    """
    Main function to orchestrate the fetching and processing of SEC filings.

    :param ticker: Company ticker symbol
    :param form: Form type to look for (e.g., '10-K')
    :param requests_per_second: Rate limit in requests per second
    """
    CIK_df = load_company_data()
    CIK = CIK_df[CIK_df["ticker"] == ticker].cik.values[0]

    form_filings = fetch_XBRL(CIK, ticker)
    print(form_filings.head(100))

    for _, row in form_filings.head(20).iterrows():
        process_filing(ticker, CIK, row)


if __name__ == "__main__":
    main(ticker, form)