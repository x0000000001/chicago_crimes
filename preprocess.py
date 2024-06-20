"""
Preprocess data to avoid repetitve computing and
allow faster diplay of figures.
"""

import datetime

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

import paths

############################################
# DATA REDUCTION
############################################


def reduce_data():
    """
    Reduce "crimes.csv" very large file into a smaller one
    by taking randomly 1 record out of 1000.
    """

    data = pd.read_csv(paths.DATA_PATH)
    data = data.sample(frac=0.001)
    data.to_csv(paths.DATA_REDUCED_PATH, index=False)


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
    if 6 <= hour < 12:
        return "Morning"
    if 12 <= hour < 18:
        return "Afternoon"
    if 18 <= hour < 24:
        return "Evening"

    raise ValueError(f"Invalid hour: {hour}")


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

    data = pd.read_csv(paths.DATA_PATH)

    for field, name, function in [
        ("Weekday", "day", weekday),
        ("Month", "month", time_of_day),
        ("Time of Day", "time_of_day", month),
    ]:
        data[field] = data["Date"].apply(function)
        crime_counts = data.groupby([field, "Primary Type"]).size().unstack()
        crime_counts["Total"] = crime_counts.iloc[:, 1:].sum(axis=1)
        crime_counts.to_csv(
            f"{paths.DATA_HISTOGRAM_FOLDER}/histogram_{name}.csv", index=False
        )


############################################
# CLUSTER PLOT
############################################


def preprocess_year(df, year):
    df_year = df[df["Year"] == year]

    # Group by 'Beat' and 'Primary Type' to get arrest counts
    grouped = (
        df_year.groupby(["Beat", "Primary Type"])
        .size()
        .reset_index(name="Arrest Count")
    )

    # Pivot table to create a matrix for clustering
    pivot_df = grouped.pivot(
        index="Beat", columns="Primary Type", values="Arrest Count"
    ).fillna(0)

    # Perform t-SNE for dimensionality reduction
    tsne = TSNE(n_components=2, random_state=0)
    tsne_result = tsne.fit_transform(pivot_df)

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=5, random_state=0)
    pivot_df["cluster"] = kmeans.fit_predict(pivot_df)

    # Create a DataFrame with t-SNE results and cluster labels
    tsne_df = pd.DataFrame(
        tsne_result, columns=["TSNE Component 1", "TSNE Component 2"]
    )
    tsne_df["cluster"] = pivot_df["cluster"].values
    tsne_df["Beat"] = pivot_df.index

    # Save the results
    tsne_df.to_csv(f"{paths.DATA_CLUSTER_FOLDER}/cluster_{year}.csv", index=False)


def preprocess_cluster():
    df = pd.read_csv(paths.DATA_PATH)

    # Convert 'Date' to datetime and extract the year
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year

    years = df["Year"].unique()

    for year in years:
        preprocess_year(df, year)

    # min and max years for the slider
    min_year = df["Year"].min()
    max_year = df["Year"].max()

    # save in file
    with open(f"{paths.DATA_CLUSTER_FOLDER}/min_max_years", "w", encoding="utf-8") as f:
        f.write(str(int(min_year)))
        f.write("\n")
        f.write(str(int(max_year)))


if __name__ == "__main__":
    preprocess_cluster()


############################################
# MAP
############################################

# TODO include map preprocessing
