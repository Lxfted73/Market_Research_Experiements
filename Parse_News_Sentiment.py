"""
This script is designed to parse and consolidate news sentiment data from JSON files within a specified folder:

- **Data Parsing:**
  - `parse_news_sentiment`: Processes raw JSON data into a pandas DataFrame:
    - Converts 'time_published' to datetime for chronological sorting.
    - Sets datetime as the index for easier time-based operations.
    - Removes less relevant columns like 'authors', 'topics', etc., to focus on key sentiment metrics.

- **File Processing:**
  - `process_file`: Reads and parses individual JSON files:
    - Handles potential errors like file not found or JSON decoding issues.

- **Folder Processing:**
  - `process_all_files_in_folder`: Iterates through all JSON files in a folder:
    - Aggregates data from multiple files into a single DataFrame for comprehensive analysis.
    - Manages exceptions for each file, ensuring only valid data is processed.

- **Execution:**
  - When run directly, it processes all JSON files in a specified folder, combining the results into one DataFrame.

This script is particularly useful for financial analysts or researchers looking to analyze aggregated news sentiment over time for stock market analysis. It supports data cleaning, time conversion, and error handling to provide a clean dataset for further analysis or visualization.
"""

import pandas as pd
import json
import os

pd.set_option('display.max_columns', None)


def parse_news_sentiment(df):
    feed_df = pd.DataFrame(df['feed'])

    # Convert 'time_published' to datetime for easier manipulation
    feed_df['datetime'] = pd.to_datetime(feed_df['time_published'], format='%Y%m%dT%H%M%S')
    feed_df.set_index('datetime', inplace=True)

    # Drop 'authors' and 'topics' columns
    feed_df = feed_df.drop(['authors', 'topics', 'banner_image',
                            'category_within_source', 'source_domain', 'url'], axis=1)
    return feed_df


def process_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return parse_news_sentiment(data)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"File at {file_path} is not valid JSON.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def process_all_files_in_folder(folder_path):
    all_data = []  # Initialize as an empty list to hold DataFrames
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.json'):  # Assuming all files of interest are JSON
            parsed_data = process_file(file_path)
            if parsed_data is not None:
                all_data.append(parsed_data)  # Append each DataFrame to the list
            else:
                print(f"Skipped file due to processing error: {filename}")

    if all_data:
        # Combine all DataFrames in the list into one DataFrame
        combined_data = pd.concat(all_data, ignore_index=False)
        return combined_data
    else:
        print("No valid data found in the folder.")
        return None


if __name__ == "__main__":
    # Example usage when running the script directly
    folder_path = 'TSM_NEWS_SENTIMENT_20240101T0000_to_20250130T0000'  # Set this to your actual folder path when testing directly
    result = process_all_files_in_folder(folder_path)