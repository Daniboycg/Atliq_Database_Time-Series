import pandas as pd
import numpy as np
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


def plot_sales_by_customer(df):
    """
    Plots the total gross sales over time for each customer in Chile.

    Parameters:
        df (pd.DataFrame): DataFrame containing at least the 'date', 'customer', and 'total_gross_sales' columns.

    Returns:
        None
    """
    # Grouping by date and customer
    sales_by_date_customer = (
        df.groupby(["date", "customer"])["total_gross_sales"].sum().reset_index()
    )
    plt.figure(figsize=(15, 7))

    # Loop over each customer to plot its time series
    for customer in sales_by_date_customer["customer"].unique():
        subset = sales_by_date_customer[sales_by_date_customer["customer"] == customer]
        plt.plot(subset["date"], subset["total_gross_sales"], label=customer)

    plt.title("Sales Over Time by Seller")
    plt.xlabel("Date")
    plt.ylabel("Total Gross Sales")
    plt.legend(loc="upper left")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()


def plot_sales_by_category_and_customer(df):
    """
    Plots the total gross sales by category and customer.

    Parameters:
        df (pd.DataFrame): DataFrame containing at least the 'category', 'customer', and 'total_gross_sales' columns.

    Returns:
        None
    """
    # Grouping by category and customer, and calculating the total gross sales
    category_sales_by_customer = (
        df.groupby(["category", "customer"])
        .agg(total_gross_sales=("total_gross_sales", "sum"))
        .reset_index()
        .sort_values("total_gross_sales", ascending=False)
    )

    # Plotting the data
    plt.figure(figsize=(14, 7))
    sns.barplot(
        data=category_sales_by_customer,
        x="category",
        y="total_gross_sales",
        hue="customer",
        palette="viridis",
    )
    plt.title("Total Gross Sales by Category and Customer in Chile")
    plt.ylabel("Total Gross Sales")
    plt.xlabel("Category")
    plt.xticks(rotation=45)
    plt.legend(title="Customer")
    plt.tight_layout()
    plt.show()


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_sales_category_matrix(df):
    """
    Plots a matrix of total gross sales by category and customer over time.

    Parameters:
        df (pd.DataFrame): DataFrame containing at least the 'date', 'category', 'customer', and 'total_gross_sales' columns.

    Returns:
        None
    """
    grouped_data = (
        df.groupby(["date", "category", "customer"])["total_gross_sales"]
        .sum()
        .reset_index()
    )
    grouped_data["date"] = pd.to_datetime(grouped_data["date"])
    grouped_data = grouped_data.sort_values(by="date")
    categories = grouped_data["category"].unique()
    n_cols = 3
    n_rows = int(np.ceil(len(categories) / n_cols))

    # Create the plot matrix
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 5 * n_rows), sharex=True)

    # Iterate over each category and place it in the matrix
    for idx, category in enumerate(categories):
        row = idx // n_cols
        col = idx % n_cols
        ax = axes[row, col]
        subset = grouped_data[grouped_data["category"] == category]
        lines = []  # Store lines for the legend
        labels = []  # Store labels for the legend
        for customer in subset["customer"].unique():
            customer_data = subset[subset["customer"] == customer]
            (line,) = ax.plot(
                customer_data["date"],
                customer_data["total_gross_sales"],
                label=customer,
                marker="o",
            )
            lines.append(line)
            labels.append(customer)
        ax.set_title(f"Sales: {category}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Sales")
        ax.grid(True)
        ax.tick_params(axis="x", rotation=45)

    # Adjust layout and add a global legend
    fig.tight_layout()
    fig.legend(
        lines, labels, loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=len(labels)
    )
    plt.show()


def plot_sales_by_category(df):
    """
    Plots total gross sales over time grouped by category and customer.

    Parameters:
        df (pd.DataFrame): DataFrame containing at least the 'date', 'category', 'customer', and 'total_gross_sales' columns.

    Returns:
        None
    """
    grouped_data = (
        df.groupby(["date", "category", "customer"])["total_gross_sales"]
        .sum()
        .reset_index()
    )
    grouped_data["date"] = pd.to_datetime(grouped_data["date"])
    grouped_data = grouped_data.sort_values(by="date")
    categories = grouped_data["category"].unique()
    line_styles = ["-", "--", "-.", ":"]

    # Set Seaborn style and color palette
    sns.set(style="whitegrid")
    palette = sns.color_palette("inferno", n_colors=len(categories))

    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 8))

    for idx, category in enumerate(categories):
        subset = grouped_data[grouped_data["category"] == category]
        for j, customer in enumerate(subset["customer"].unique()):
            customer_data = subset[subset["customer"] == customer]
            sns.lineplot(
                data=customer_data,
                x="date",
                y="total_gross_sales",
                label=f"{category} - {customer}",
                color=palette[idx],
                linestyle=line_styles[j % len(line_styles)],
                ax=ax,
            )

    ax.set_title("Atliq Sales in Chile Over Time by Category and Customer")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Sales")
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    ax.grid(True)
    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()
