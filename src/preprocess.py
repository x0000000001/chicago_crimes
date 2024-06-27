"""
Preprocess data to avoid repetitve computing and
allow faster diplay of figures.
"""

import datetime

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

import paths as paths

############################################
# DATA REDUCTION
############################################


def reduce_data():
    """
    Reduce "crimes.csv" very large file into a smaller one
    by taking randomly 1 record out of 1000.
    """

    data = pd.read_csv(paths.DATA_PATH)
    data = data.sample(frac=0.1)
    data.to_csv("reduced10.csv", index=False)


############################################
# HISTOGRAM
############################################

CRIMES_CATEGORIES = {
    "Violent": [
        "BATTERY",
        "ROBBERY",
        "ASSAULT",
        "CRIMINAL SEXUAL ASSAULT",
        "CRIM SEXUAL ASSAULT",
        "STALKING",
        "HOMICIDE",
        "KIDNAPPING",
        "SEX OFFENSE",
        "INTIMIDATION",
        "DOMESTIC VIOLENCE",
    ],
    "Property": [
        "THEFT",
        "CRIMINAL DAMAGE",
        "BURGLARY",
        "MOTOR VEHICLE THEFT",
        "CRIMINAL TRESPASS",
        "ARSON",
    ],
    "Crimes Against Children": ["OFFENSE INVOLVING CHILDREN"],
    "Miscellaneous": [
        "OTHER OFFENSE",
        "INTERFERENCE WITH PUBLIC OFFICER",
        "NON-CRIMINAL",
        "HUMAN TRAFFICKING",
        "NON-CRIMINAL (SUBJECT SPECIFIED)",
        "NON - CRIMINAL",
        "RITUALISM",
    ],
    "Public Order": [
        "WEAPONS VIOLATION",
        "PROSTITUTION",
        "PUBLIC PEACE VIOLATION",
        "CONCEALED CARRY LICENSE VIOLATION",
        "LIQUOR LAW VIOLATION",
        "OBSCENITY",
        "GAMBLING",
        "PUBLIC INDECENCY",
    ],
    "Drug Offenses": ["NARCOTICS", "OTHER NARCOTIC VIOLATION"],
    "White Collar": ["DECEPTIVE PRACTICE"],
}


def weekday(date):
    date = datetime.datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p")
    return date.strftime("%A")


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
    return date.strftime("%B")


TIME_ORDERS = {
    "Weekday": [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ],
    "Month": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
    "Time of Day": ["Morning", "Afternoon", "Evening", "Night"],
}


def preprocess_histogram():
    """
    Aggregates crimes count by :
    * crime types according to the "Primary Type" field.
    * time period according to the"Date" field in three different ways :
        - times of the day (morning, afternoon, evening, night)
        - days of the week
        - months according to the "Date" field
    """

    data = pd.read_csv(paths.DATA_REDUCED_PATH)

    # change data "Primary Type" field according to the CRIMES_CATEGORIES
    # for category, crimes in CRIMES_CATEGORIES.items():
    #     data.loc[data["Primary Type"].isin(crimes), "Primary Type"] = category

    for field, name, function in [
        ("Weekday", "day", weekday),
        ("Month", "month", month),
        ("Time of Day", "time_of_day", time_of_day),
    ]:
        data[field] = data["Date"].apply(function)
        crime_counts = data.groupby([field, "Primary Type"]).size().unstack()
        crime_counts.insert(0, name, crime_counts.index)
        crime_counts["Total"] = crime_counts.iloc[:, 1:].sum(axis=1)
        crime_counts = crime_counts.reindex(TIME_ORDERS[field])
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
    # preprocess_histogram()
    reduce_data()


############################################
# MAP
############################################

# TODO include map preprocessing
