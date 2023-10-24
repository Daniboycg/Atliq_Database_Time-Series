import pandas as pd
import numpy as np

pd.set_option("display.max_rows", 50)
pd.set_option("display.max_columns", 50)
pd.options.display.float_format = "{:,.2f}".format
import matplotlib.pyplot as plt
import seaborn as sns


def plot_time_series_sales(
    df,
    date_col,
    sales_col,
    title="Plots a time series of LATAM Total Sales of AtliQ Hardware from 2017-2021",
):
    """
    Plots a time series of LATAM Total Sales of AtliQ Hardware from 2017-2021.

    Parameters:
    - data (DataFrame): The data containing the sales and date information.
    - date_col (str): The name of the column with date data.
    - sales_col (str): The name of the column with sales data.
    - title (str): The title for the plot. Default is 'Total Sales over Time'.
    """

    # Aggregating the data
    time_series_data = df.groupby(date_col)[sales_col].sum().reset_index()

    # Plotting
    plt.figure(figsize=(15, 7))
    sns.lineplot(data=time_series_data, x=date_col, y=sales_col)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Total Gross Sales")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()


def plot_moving_average(
    df, date_col, sales_col, window=6, title="Total Sales with Moving Average"
):
    """
    Plots original sales data and its moving average.

    Parameters:
    - df (DataFrame): The data containing the sales and date information.
    - date_col (str): The name of the column with date data.
    - sales_col (str): The name of the column with sales data.
    - window (int): The size of the moving average window. Default is 6.
    - title (str): The title for the plot. Default is 'Total Sales with Moving Average'.
    """

    # Aggregating the data
    time_series_data = df.groupby(date_col)[sales_col].sum().reset_index()
    time_series_data[f"{window}_month_MA"] = (
        time_series_data[sales_col].rolling(window=window).mean()
    )

    # Plotting
    plt.figure(figsize=(15, 7))

    # Original data
    sns.lineplot(df=time_series_data, x=date_col, y=sales_col, label="Original Data")

    # Moving average
    sns.lineplot(
        df=time_series_data,
        x=date_col,
        y=f"{window}_month_MA",
        label=f"{window}-Month Moving Average",
        color="red",
    )

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Total Gross Sales")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()
