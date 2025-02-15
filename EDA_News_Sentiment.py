"""
This script processes and visualizes news sentiment data for a specified stock ticker:

- **Data Processing:**
  - Uses a custom function `process_all_files_in_folder` from 'Parse_News_Sentiment' to load and parse news sentiment data from a designated folder path.

- **Data Inspection:**
  - Checks if the data was successfully loaded and prints basic information about the dataset, including the first few rows and dataset structure.

- **Visualization:**
  - Utilizes Plotly Express for creating an interactive scatter plot:
    - Plots the 'overall_sentiment_score' over time.
    - Colors points by 'source' if available, enhancing differentiation of sentiment by news provider.
    - Includes enhancements like title positioning, grid lines for better readability, date formatting, and a range slider for temporal exploration.

- **Interactive Features:**
  - Implements scroll and zoom functionalities, along with a comprehensive set of controls in the plot's mode bar for user interaction with the data visualization.

- **Configuration:**
  - Sets up Pandas to display all columns for comprehensive data inspection.
  - Defines file paths and ticker symbols dynamically from file names for flexibility.

This script is designed for financial analysts or researchers to explore how news sentiment changes over time for a particular stock, potentially aiding in market analysis or investment decisions.
"""

from Parse_News_Sentiment import process_all_files_in_folder as parse_news_sentiment
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

pd.set_option('display.max_columns', None)

# Set the file paths
file_path_news_sentiment = 'TSM_NEWS_SENTIMENT_20240101T0000_to_20250130T0000'
ticker = file_path_news_sentiment[:3]

# Load the datasets
df_news_sentiment = parse_news_sentiment(file_path_news_sentiment)

# Check loaded data
if df_news_sentiment is not None:
    print(f"{ticker} News Sentiment Data:")
    print(df_news_sentiment.head())
    print(df_news_sentiment.info())
else:
    print(f"Failed to process{ticker}df_news_sentiment.")

fig = px.scatter(df_news_sentiment,
                 x=df_news_sentiment.index,
                 y="overall_sentiment_score",
                 color="source" if 'source' in df_news_sentiment.columns else None,
                 title="Sentiment Distribution Over Time",
                 labels={'datetime': 'Date', 'overall_sentiment_score': 'Sentiment Score'},
                 )

# Enhancements for better readability and scrolling/zooming:
fig.update_layout(
    title={
        'text': "Sentiment Distribution Over Time",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title="Date",
    yaxis_title="Sentiment Score",
    font=dict(size=14),
    xaxis=dict(
        showgrid=True,
        gridcolor='lightgrey',
        tickfont=dict(size=12),
        tickangle=45,  # Angle for better readability if many dates
        rangeslider=dict(visible=True),  # Adds a range slider for x-axis
        type="date"  # Ensures date format for the x-axis
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgrey',
        tickfont=dict(size=12),
        range=[df_news_sentiment['overall_sentiment_score'].min() - 0.1,  # Adjust this range based on your data
               df_news_sentiment['overall_sentiment_score'].max() + 0.1]
    ),
    legend_title_text='Source',
    legend=dict(
        orientation="h",  # Horizontal legend for space efficiency
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    dragmode='zoom',  # Default interaction to zoom
    hovermode='closest'  # Shows hover info for the closest point to the cursor
)

# To ensure zooming functionality with additional features
fig.show(config={
    'scrollZoom': True,
    'displayModeBar': True,
    'modeBarButtonsToAdd': ['zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
})



