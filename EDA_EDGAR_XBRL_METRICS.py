"""
This script processes and visualizes financial metrics from EDGAR XBRL filings for a specified company:

- **Data Extraction:**
  - Uses `extract_metrics_from_EDGAR_XBRL` to fetch financial metrics from SEC filings.
  - Focuses on a predefined list of key financial metrics ('top_25_metrics').

- **Data Processing:**
  - Sorts and filters data by 'content' to create separate DataFrames for each metric.
  - Specifically processes:
    - **Revenue** (`process_df_0`):
      - Calculates growth rates, distributes revenue over time, and computes cumulative revenue.
    - **Cost of Goods and Services Sold (COGS)** (`process_df_1`):
      - Focuses on 10-Q filings, computes cumulative and non-cumulative COGS over time.

- **Visualization:**
  - Utilizes Plotly for creating interactive plots:
    - `plot_df_0_cumulative_revenue`: Visualizes both cumulative and monthly revenue over time.
    - `plot_df_1_cogs`: Plots cumulative and non-cumulative COGS, providing insights into cost trends.

- **Utility Functions:**
  - Functions for processing individual metrics include data cleaning, aggregation, and transformation to fit analytical needs.

- **Execution:**
  - Processes data for the ticker 'PLTR' for the year 2020 by default, though this can be adjusted.
  - The script demonstrates how to handle, analyze, and visualize financial data from public filings, offering a template for financial analysis of other companies or metrics.

This script is valuable for financial analysts, investors, or researchers looking to analyze company financial health over time using SEC data.
"""

from EDA_EDGAR_XBRL import extract_metrics_from_EDGAR_XBRL
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

ticker = "PLTR"
start_year = "2020"
end_year = "2020"
print_extra = False
top_25_metrics = [
    'us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax_USD', #df_0
    'us-gaap_CostOfGoodsAndServicesSold_USD', #df_1
    'us-gaap_ResearchAndDevelopmentExpense_USD',
    'us-gaap_NetIncomeLoss_USD',
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
    'us-gaap_AllocatedShareBasedCompensationExpense_USD'
]

data = extract_metrics_from_EDGAR_XBRL(ticker)
df = pd.DataFrame(data)
# First, sort the DataFrame
df_sorted = df.sort_values(by='content')
# Get unique values in 'content'
unique_contents = df_sorted['content'].unique()
# Dictionary to hold separate DataFrames
content_dfs = {}
# Loop through the metrics list to create separate DataFrames
for metric in top_25_metrics:
    # Filter DataFrame for each metric
    # This will only include metrics that exist in df_sorted
    if metric in df_sorted['content'].values:
        content_dfs[metric] = df_sorted[df_sorted['content'] == metric].copy()
    else:
        # If the metric doesn't exist in df_sorted, we can create an empty DataFrame or skip it
        content_dfs[metric] = pd.DataFrame()  # Creates an empty DataFrame
        # or
        # print(f"Warning: Metric '{metric}' not found in the DataFrame.")



#'us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax_USD',
def process_df_0(df, print_extra=False):
    if 'us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax_USD' in df['content'].values:
        content_row = df[df['content'] == 'us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax_USD'].iloc[0]
        print(f"Content found: {content_row}")
    else:
        print("us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax_USD not found")
        return
    if print_extra:
        print(df.head())
        print(df.info())
        print(df['content'])
        print(f"df_0 = {content_row}")

    df['growth_rate'] = df['val'].pct_change() * 100

    def distribute_revenue(row):
        # Create a range from start to end date
        start_date = pd.to_datetime(row['start'])
        end_date = pd.to_datetime(row['end'])
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')

        # Calculate the number of days the revenue spans
        days = len(date_range)

        # Daily revenue allocation
        daily_revenue = row['val'] / days

        # Distribute revenue to each day, then sum by month
        monthly_allocation = {}
        for date in date_range:
            month = date.to_period('M')
            if month not in monthly_allocation:
                monthly_allocation[month] = 0
            monthly_allocation[month] += daily_revenue

        return pd.Series(monthly_allocation)

    # Apply the function to each row
    monthly_revenues = df.apply(distribute_revenue, axis=1)

    # Sum up all revenues for each month
    cumulative_revenues = monthly_revenues.sum().sort_index()

    # Create full date range for all months
    start_column = pd.to_datetime(df['start'])
    end_column = pd.to_datetime(df['end'])
    full_date_range = pd.period_range(start=start_column.min().to_period('M'),
                                      end=end_column.max().to_period('M'),
                                      freq='M')

    # Convert cumulative_revenues to DataFrame
    cumulative_df = pd.DataFrame({'revenue': cumulative_revenues}).reindex(full_date_range).fillna(0)
    cumulative_df = cumulative_df.sort_index()

    # Calculate cumulative sum
    cumulative_df['cumulative_revenue'] = cumulative_df['revenue'].cumsum()

    # Convert period index to timestamp for 'end' column
    cumulative_df['end'] = cumulative_df.index.to_timestamp()

    plot_df_0_cumulative_revenue(cumulative_df)

    return cumulative_df[['end', 'revenue', 'cumulative_revenue']]


#'us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax_USD',
def plot_df_0_cumulative_revenue(cumulative_df):
    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Ensure 'end' is datetime and sort by date
    cumulative_df['end'] = pd.to_datetime(cumulative_df['end'])
    cumulative_df = cumulative_df.sort_values('end')

    # Create the figure with subplots
    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,  # Share the x-axis for both plots
                        vertical_spacing=0.3,
                        subplot_titles=("Cumulative Revenue", "Monthly Revenue"))

    # Add trace for cumulative revenue
    fig.add_trace(go.Scatter(
        x=cumulative_df['end'],
        y=cumulative_df['cumulative_revenue'],
        mode='lines+markers',
        name='Cumulative Revenue',
        line=dict(color='blue')
    ), row=1, col=1)

    # Add trace for monthly revenue
    fig.add_trace(go.Scatter(
        x=cumulative_df['end'],
        y=cumulative_df['revenue'],
        mode='lines+markers',
        name='Monthly Revenue',
        line=dict(color='red')
    ), row=2, col=1)

    # Update layout for both plots
    fig.update_layout(
        title_text='Revenue Over Time',
        height=1000,  # Adjusted height to accommodate two subplots
        width=1000,
        showlegend=False,  # Legends are shown in each subplot
        xaxis_tickangle=-45
    )

    # Update x-axis for both subplots
    for i in [1, 2]:
        fig.update_xaxes(
            title_text='Date',
            gridcolor='lightgrey',
            gridwidth=0.5,
            rangeslider=dict(
                visible=True
            ),
            type="date",
            row=i, col=1
        )

    # Update y-axis for both subplots
    fig.update_yaxes(
        title_text='Cumulative Revenue',
        gridcolor='lightgrey',
        gridwidth=0.5,
        tickformat=',.0f',  # Format for whole numbers with commas
        row=1, col=1
    )
    fig.update_yaxes(
        title_text='Monthly Revenue',
        gridcolor='lightgrey',
        gridwidth=0.5,
        tickformat=',.0f',  # Format for whole numbers with commas
        row=2, col=1
    )

    # Show the plot
    fig.show()

#us-gaap_CostOfGoodsAndServicesSold_USD
def process_df_1(df_1):
    if 'us-gaap_CostOfGoodsAndServicesSold_USD' in df['content'].values:
        content_row = df[df['content'] == 'us-gaap_CostOfGoodsAndServicesSold_USD'].iloc[0]
        print(f"Content found: {content_row}")
    else:
        print("us-gaap_CostOfGoodsAndServicesSold_USD not found")
        return

    # Filter for only 10-Q forms right at the beginning for efficiency
    df_1 = df_1.loc[df_1['form'] == '10-Q'].copy()  # Use .loc and .copy() for clarity

    # Convert 'end' to datetime if it's not already (assuming 'end' is your key for accumulation)
    df_1['end'] = pd.to_datetime(df_1['end'])


    # Sort DataFrame by 'end' in ascending order
    df_sorted = df_1.sort_values('end')

    # Drop rows with duplicate 'end' and 'val'
    df_sorted.drop_duplicates(subset=['end', 'val'], inplace=True)

    # Calculate cumulative sum of 'val' which we assume represents COGS
    df_sorted.loc[:, 'cogs_cumulative'] = df_sorted['val'].cumsum()

    # Add the non-cumulative COGS as a column (assuming 'val' is COGS for each period)
    df_sorted.loc[:, 'cogs'] = df_sorted['val']

    # If you want only the 'end', cumulative COGS, and non-cumulative COGS:
    result = df_sorted[['end', 'cogs', 'cogs_cumulative']]

    # Set 'end' as index for a time series-like presentation
    result.set_index('end', inplace=True)

    return result

#us-gaap_CostOfGoodsAndServicesSold_USD
def plot_df_1_cogs(df_1):
    """
    Plot both non-accumulated and cumulative COGS values over time.

    Parameters:
    - df: DataFrame with 'cogs' (non-cumulative) and 'cogs_cumulative' columns,
          and datetime index.

    Returns:
    - Displays a Plotly figure.
    """
    # Create a figure with two subplots
    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=("Cumulative COGS", "Non-Cumulative COGS"),
                        vertical_spacing=0.3)

    # Add trace for cumulative COGS in the first subplot
    fig.add_trace(
        go.Scatter(
            x=df_1.index,
            y=df_1['cogs_cumulative'],
            mode='lines+markers',
            name='Cumulative COGS',
            line=dict(color='red')
        ),
        row=1,  # specifying the first row
        col=1
    )

    # Add trace for non-cumulative COGS in the second subplot
    fig.add_trace(
        go.Scatter(
            x=df_1.index,
            y=df_1['cogs'],
            mode='lines+markers',
            name='Non-Cumulative COGS',
            line=dict(color='blue')
        ),
        row=2,  # specifying the second row
        col=1
    )

    # Update layout for each subplot
    fig.update_layout(
        title='COGS Over Time',
        height=1000,  # Increased height to accommodate two subplots
        width=1000,
        legend_title_text='COGS Type',
        dragmode='zoom',
        hovermode='x unified'
    )

    # Update x-axis for both subplots
    for i in [1, 2]:
        fig.update_xaxes(
            title_text='Date',
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True,
                thickness=0.1,
                bgcolor="LightGrey"
            ),
            type="date",
            autorange=True,
            range=[df_1.index.min(), df_1.index.max()],
            rangeslider_autorange=True,
            row=i, col=1
        )

    # Update y-axis for both subplots
    for i in [1, 2]:
        fig.update_yaxes(
            title_text='COGS (USD)',
            type='linear',
            autorange=True,
            rangemode='tozero',
            tickformat=',d',
            showgrid=True,
            gridcolor='LightGrey',
            zeroline=True,
            zerolinecolor='LightGrey',
            ticks="outside",
            row=i, col=1
        )

    # Show plot
    fig.show()


if __name__ == "__main__":

    # Example usage:
    # Assuming df_1 has 'end' and 'cogs_cumulative' columns after processing:
    df_0 = content_dfs[list(content_dfs.keys())[0]]
    df_1 = content_dfs[list(content_dfs.keys())[1]]
    df_2 = content_dfs[list(content_dfs.keys())[2]]

    df_0 = process_df_0(df_0)
    df_1 = process_df_1(df_1)

    # Assuming you want to plot with the same DataFrame, use df_1 here as well
    plot_df_1_cogs(df_1)

