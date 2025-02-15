"""
This script analyzes OHLCV (Open, High, Low, Close, Volume) data for a stock across multiple years, focusing on:

- **Data Parsing:**
  - Utilizes a custom function `parse_ohlcv_folder` from 'Parse_OHCLV' to read OHLCV data for each year.

- **Data Visualization:**
  - Employs Plotly for creating interactive time series plots of closing prices.
  - Generates plots for each year within a specified range, showcasing stock price evolution over time.

- **Functionality:**
  - `analyze_ohlcv_data_for_years` function:
    - Iterates through years from `start_year` to `end_year`.
    - Parses data for each year from a specified file path format.
    - Checks for the presence of a 'datetime' column to ensure plot viability.
    - Plots the closing price over time with interactive features like zoom, range selection, and hover information.

- **Additional Features (Commented Out):**
  - Includes commented-out code for further analysis like distribution plots and correlation heatmaps.

- **Usage:**
  - Takes a stock ticker, start year, and end year as parameters to analyze and visualize data.

The script is tailored for financial analysis, providing visual insights into stock price trends over multiple years.
"""

from Parse_OHCLV import parse_ohlcv_folder as parse_ohlcv
import plotly.graph_objects as go

def analyze_ohlcv_data_for_years(ticker, start_year, end_year):
    """
    Analyzes OHLCV data for a given ticker over a range of years, plotting time series.

    :param ticker: The stock ticker symbol (e.g., 'TSM').
    :param start_year: The starting year for analysis.
    :param end_year: The ending year for analysis.
    :return: None
    """
    for year in range(start_year, end_year + 1):
        file_path = f'{ticker}_TIME_SERIES_INTRADAY_5min_adjustedfalse_extendedtrue_year{year}'

        # Parse the OHLCV data for each year
        data_ohlcv = parse_ohlcv(file_path)

        if data_ohlcv is not None:
            print(f"\nOHLCV Data for {ticker} in {year}:")
            print(data_ohlcv.head())
            print(data_ohlcv.info())

            # Plotting OHLCV data over time
            if 'datetime' not in data_ohlcv.columns:
                print(f"No 'datetime' column found in DataFrame for {year}. Skipping year.")
                continue
            else:
                # Create the plot
                fig = go.Figure(data=[go.Scatter(x=data_ohlcv['datetime'],
                                                 y=data_ohlcv['4. close'],
                                                 mode='lines',
                                                 name=f'{year} Close Price')])

                # Customize layout
                fig.update_layout(
                    title=f'{ticker} Stock Price Over Time - {year}',
                    xaxis_title='Time',
                    yaxis_title='Price',
                    hovermode='x unified'  # Makes hover info group by x-value
                )
                # Enable zooming and other interactions
                fig.update_xaxes(rangeslider_visible=True)  # Adds a range slider for zooming
                fig.update_layout(
                    xaxis=dict(
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label="1m", step="month", stepmode="backward"),
                                dict(count=6, label="6m", step="month", stepmode="backward"),
                                dict(count=1, label="YTD", step="year", stepmode="todate"),
                                dict(count=1, label="1y", step="year", stepmode="backward"),
                                dict(step="all")
                            ])
                        )
                    )
                )

                # Show the plot
                fig.show()

                # Commented out for now, but available for additional analysis
                # Distribution of Closing Prices
                # plt.figure(figsize=(10, 6))
                # sns.histplot(data_ohlcv['4. close'], kde=True, bins=30)
                # plt.title(f'Distribution of Closing Prices - {year}')
                # plt.xlabel('Closing Price')
                # plt.ylabel('Frequency')
                # plt.show()
                #
                # # Correlation Heatmap for OHLCV data
                # plt.figure(figsize=(10, 8))
                # sns.heatmap(data_ohlcv.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
                # plt.title(f'Correlation Heatmap of OHLCV Data - {year}')
                # plt.show()
        else:
            print(f"No data for {file_path} in year {year}")


# Example usage
ticker = 'AMD'
start_year = 2019
end_year = 2024
analyze_ohlcv_data_for_years(ticker, start_year, end_year)