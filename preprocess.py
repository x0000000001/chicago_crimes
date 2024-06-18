"""
Preprocess data to avoid repetitve computing and 
allow faster diplay of figures.
"""

import pandas as pd
import datetime

DATA_FOLDER = "assets/data"
DATA_PATH = f"{DATA_FOLDER}/crimes.csv"
DATA_REDUCED_PATH = f"{DATA_FOLDER}/crimes_reduced.csv"  # 1000 times reduced dataset

HISTOGRAM_MONTHS_PATH = f"{DATA_FOLDER}/histogram_months.csv"
HISTOGRAM_DAYS_PATH = f"{DATA_FOLDER}/histogram_days.csv"
HISTOGRAM_TIME_OF_DAY_PATH = f"{DATA_FOLDER}/histogram_times_of_day.csv"


############################################
# DAT REDUCTION
############################################


def reduce_data():
    """
    Reduce "crimes.csv" very large file into a smaller one
    by taking randomly 1 record out of 1000.
    """

    data = pd.read_csv(DATA_PATH)
    data = data.sample(frac=0.001)
    data.to_csv(DATA_REDUCED_PATH, index=False)


############################################
# HISTOGRAM
############################################


def weekday(date):
    date = datetime.datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p")
    return date.weekday()


def time_of_day(date):
    date = datetime.datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p")
    hour = date.hour
    if 0 <= hour < 6:
        return "Night"
    elif 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"


def month(date):
    date = datetime.datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p")
    return date.month


def preprocess_histogram():
    """
    Aggregates crimes count by :
    * crime types according to the "Primary Type" field.
    * time period according to the"Date" field in three different ways :
        - times of the day (morning, afternoon, evening, night)
        - days of the week
        - months according to the "Date" field
    """

    data = pd.read_csv(DATA_PATH)

    # Extract the date column from the data
    data["Weekday"] = data["Date"].apply(weekday)
    data["Time of Day"] = data["Date"].apply(time_of_day)
    data["Month"] = data["Date"].apply(month)

    # Time of the day
    crime_counts = data.groupby(["Time of Day", "Primary Type"]).size().unstack()
    # Save the processed data
    crime_counts.to_csv(HISTOGRAM_TIME_OF_DAY_PATH)

    # Days of the week
    crime_counts = data.groupby(["Weekday", "Primary Type"]).size().unstack()
    # Save the processed data
    crime_counts.to_csv(HISTOGRAM_DAYS_PATH)

    # Months
    crime_counts = data.groupby(["Month", "Primary Type"]).size().unstack()
    # Save the processed data
    crime_counts.to_csv(HISTOGRAM_MONTHS_PATH)


def compute_totals():
    # Total
    histogram_months = pd.read_csv(HISTOGRAM_MONTHS_PATH)
    histogram_days = pd.read_csv(HISTOGRAM_DAYS_PATH)
    histogram_time_of_day = pd.read_csv(HISTOGRAM_TIME_OF_DAY_PATH)

    histogram_months["Total"] = histogram_months.iloc[:, 1:].sum(axis=1)
    histogram_days["Total"] = histogram_days.iloc[:, 1:].sum(axis=1)
    histogram_time_of_day["Total"] = histogram_time_of_day.iloc[:, 1:].sum(axis=1)

    histogram_months.to_csv(HISTOGRAM_MONTHS_PATH, index=False)
    histogram_days.to_csv(HISTOGRAM_DAYS_PATH, index=False)
    histogram_time_of_day.to_csv(HISTOGRAM_TIME_OF_DAY_PATH, index=False)


if __name__ == "__main__":
    compute_totals()
