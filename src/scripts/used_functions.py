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


def plot_sales_with_moving_average(df):
    """
    Plots the total gross sales over time along with a 6-month moving average.

    Parameters:
        df (pd.DataFrame): DataFrame containing at least the 'date' and 'total_gross_sales' columns.

    Returns:
        None
    """
    # Grouping and calculating the moving average
    time_series_data = df.groupby("date")["total_gross_sales"].sum().reset_index()
    time_series_data["6_month_MA"] = (
        time_series_data["total_gross_sales"].rolling(window=6).mean()
    )

    # Plotting
    plt.figure(figsize=(15, 7))

    # Original data
    sns.lineplot(
        data=time_series_data, x="date", y="total_gross_sales", label="Original Data"
    )

    # 6-month moving average
    sns.lineplot(
        data=time_series_data,
        x="date",
        y="6_month_MA",
        label="6-Month Moving Average",
        color="red",
    )

    plt.title("AtliQ Sales in LATAM with 6-Month Moving Average")
    plt.xlabel("Date")
    plt.ylabel("Total Gross Sales")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_sales_by_market(df):
    """
    Plots the total gross sales over time for each market (country).

    Parameters:
        df (pd.DataFrame): DataFrame containing at least the 'date', 'market', and 'total_gross_sales' columns.

    Returns:
        None
    """
    # Grouping by date and market
    sales_by_date_market = (
        df.groupby(["date", "market"])["total_gross_sales"].sum().reset_index()
    )

    # Plotting
    plt.figure(figsize=(15, 7))

    # Loop over each market to plot its time series
    for market in sales_by_date_market["market"].unique():
        subset = sales_by_date_market[sales_by_date_market["market"] == market]
        plt.plot(subset["date"], subset["total_gross_sales"], label=market)

    plt.title("Sales Over Time by Market (Country)")
    plt.xlabel("Date")
    plt.ylabel("Total Gross Sales")
    plt.legend(loc="upper left")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()
