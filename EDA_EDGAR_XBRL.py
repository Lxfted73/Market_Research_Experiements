"""
This script integrates financial data from EDGAR XBRL filings with OHLCV stock data for analysis:

- **Data Acquisition:**
  - `acquire_xbrl_data`: Fetches XBRL financial data for a given ticker using `parse_EDGAR_XBRL_all`.
  - `acquire_ohclv_data`: Retrieves OHLCV (Open, High, Low, Close, Volume) stock data from a specific folder, using `parse_ohlcv_folder`.

- **Date Handling:**
  - `next_trading_day`: Calculates the next valid trading day, skipping weekends.
  - `shift_to_market_open`: Converts a filing date to the next market open time (9:30 AM), adjusting for weekends.

- **Data Processing:**
  - `extract_metrics`:
    - Extracts financial metrics from the XBRL data for a predefined list of metrics.
    - Adds a 'market_day' to align financial events with trading days, facilitating correlation with stock data.
    - Handles potential date parsing errors and missing data.

- **Metric Extraction:**
  - `extract_metrics_from_EDGAR_XBRL`: Orchestrates the extraction process for a specific ticker, focusing on the 'top_25_metrics' list.

- **Utility and Configuration:**
  - Various flags (`print_gaap_keys`, `print_metrics`, etc.) for debugging and logging purposes.
  - Configuration variables for the ticker, year range, and metrics to be analyzed.

- **Execution:**
  - When run, it processes the XBRL data for "PLTR" over a specified period, preparing it for further analysis like correlating with stock price movements.

This script is designed for financial analysts or data scientists looking to combine fundamental financial data with stock market data to analyze the impact of financial disclosures on stock prices or to perform comprehensive financial analysis.
"""

from Parse_EDGAR_XBRL import parse_EDGAR_XBRL_all
from Parse_OHCLV import parse_ohlcv_folder
from datetime import datetime, timedelta, time

print_gaap_keys = False
print_metrics = False
print_added_row = False
print_namespace_data = False
print_cannot_find_valid_tradings_days = False
correlation_days_comparison = 10
ticker = "PLTR"
start_year = 2019
end_year = 2025
top_25_metrics = [
    'us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax_USD',
    'us-gaap_CostOfGoodsAndServicesSold_USD',
    'us-gaap_ResearchAndDevelopmentExpense_USD'
    'us-gaap_NetIncomeLoss_USD',
    'us-gaap_EarningsPerShareBasic_USD/shares',
    'us-gaap_EarningsPerShareDiluted_USD/shares',
    'us-gaap_OperatingIncomeLoss_USD',
    'us-gaap_GrossProfit_USD',
    'us-gaap_Assets_USD',
    'us-gaap_AssetsCurrent_USD',
    'us-gaap_LiabilitiesCurrent_USD',
    'us-gaap_StockholdersEquity_USD',
    'us-gaap_CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents_USD',
    'us-gaap_CashAndCashEquivalentsAtCarryingValue_USD',
    'us-gaap_CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect_USD',
    'us-gaap_NetCashProvidedByUsedInOperatingActivities_USD',
    'us-gaap_NetCashProvidedByUsedInInvestingActivities_USD',
    'us-gaap_NetCashProvidedByUsedInFinancingActivities_USD',
    'us-gaap_InterestExpense_USD',
    'us-gaap_LongTermDebt_USD',
    'us-gaap_DebtInstrumentCarryingAmount_USD',
    'us-gaap_AllocatedShareBasedCompensationExpense_USD',
    'us-gaap_ShareBasedCompensation_USD',
    'us-gaap_IncomeTaxExpenseBenefit_USD',
    'us-gaap_ResearchAndDevelopmentExpense_USD',
    'us-gaap_SellingGeneralAndAdministrativeExpense_USD',
    'us-gaap_InventoryNet_USD'
]
def acquire_xbrl_data(ticker):
    dict = parse_EDGAR_XBRL_all(ticker)
    print(f"Acquired XBRL data for {ticker}")
    if print_gaap_keys:
        for concept in list(dict['us-gaap'].keys()):
            print(concept)
    return dict

def acquire_ohclv_data(folder_path):
    df = parse_ohlcv_folder(folder_path)
    print(f"Acquired OHLCV data from {folder_path}")
    return df

def next_trading_day(date):
    date += timedelta(days=1)
    while date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
        date += timedelta(days=1)
    return date

def shift_to_market_open(filing_date):
    """
    Shift a given filing date to the next market open time (assumed 9:30 AM for U.S. markets).

    Parameters:
    - filing_date (datetime.date): The date of the filing.

    Returns:
    - datetime.datetime: The datetime set to the next market open after the filing date.
    """
    # Combine the date with the market open time
    market_open_time = time(9, 30)  # 9:30 AM
    market_open_datetime = datetime.combine(filing_date, market_open_time)

    # If the filing was on a weekend, move to the next Monday
    if market_open_datetime.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
        market_open_datetime = market_open_datetime + timedelta(days=7 - market_open_datetime.weekday())

    return market_open_datetime

def extract_metrics(xbrl_data, metrics_list):
    """
    Extract data for specified financial metrics from XBRL data, adding a market day value.

    Parameters:
    - xbrl_data: Dictionary containing parsed XBRL data.
    - metrics_list: List of GAAP metric keys to consider.

    Returns:
    - List of dictionaries: Each dictionary contains the original data plus 'market_day'.
    """
    metrics_data = []
    print(f"Processing {len(metrics_list)} metrics.")

    for metric in metrics_list:
        if print_metrics == True:
            print(f"Looking for metric: {metric}")
        for namespace in list(xbrl_data.keys()):
            if print_metrics == True:
                print(f"Checking namespace: {namespace}")
            if metric in xbrl_data[namespace]:
                if print_metrics == True:
                    print(f"Found metric {metric} in namespace {namespace}")
                for namespace_data in xbrl_data[namespace][metric]:  # Assuming items are under each metric
                    if print_namespace_data == True:
                        print(f"Data for {metric}: {namespace_data}")
                    if 'filed' in namespace_data:
                        try:
                            # Parse the filing date
                            filing_date = datetime.strptime(namespace_data['filed'], '%Y-%m-%d').date()
                            # Adjust to market open time
                            market_day = shift_to_market_open(filing_date)

                            # Construct row with all available data plus market day
                            row = dict(namespace_data)
                            row['market_day'] = market_day
                            row['namespace'] = namespace
                            row['content'] = metric
                            # Add the adjusted market day
                            metrics_data.append(row)
                            if print_added_row == True:
                                print(f"Added data: {row}")
                        except ValueError as e:
                            print(f"Could not parse date: {namespace_data.get('filed', 'No filed date')}. Error: {e}")
                    else:
                        print(f"Item missing 'filed': {namespace_data}")
            else:
                if print_metrics == True:
                    row = dict()
                    row['content'] = metric
                    metrics_data.append(row)
                    print(f"Metric {metric} not found in namespace {namespace}")

    print(f"Total items collected: {len(metrics_data)}")
    return metrics_data

def extract_metrics_from_EDGAR_XBRL(ticker):
    xbrl_data = acquire_xbrl_data(ticker)
    metrics_data = extract_metrics(xbrl_data, top_25_metrics)
    return metrics_data

if __name__ == "__main__":
    extract_metrics_from_EDGAR_XBRL(ticker)
