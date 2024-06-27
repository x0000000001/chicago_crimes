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

# File paths
geojson_path_beatsdistricts = 'src/data/map/Police_Beat_Boundary_View.geojson'
geojson_path_neighborhoods = 'src/data/map/district_neighborhoods.json'

# Load the reduces data with the required columns 
columns_to_load = ['Date', 'Block', 'Primary Type', 'Description', 'Location Description', 'Arrest', 'Beat', 'Year', 'Updated On', 'Latitude', 'Longitude']
df_map = pd.read_csv(paths.DATA_PATH, usecols=columns_to_load)
new_column_names = ['date', 'block', 'primary_type', 'description', 'location_description', 'arrest', 'beat', 'year', 'updated_on', 'latitude', 'longitude']
df_map.columns = new_column_names

# Convert the date column to datetime type
df_map['date'] = pd.to_datetime(df_map['date'])

# Extract month, day of the week, and hour from the date column
df_map['month'] = df_map['date'].dt.strftime('%B')
df_map['day_of_week'] = df_map['date'].dt.strftime('%A')
df_map['hour'] = df_map['date'].dt.hour
df_map['beat'] = df_map['beat'].astype(str)
# Load the GeoJSON files
with open(geojson_path_beatsdistricts) as f:
    geojson_beats = json.load(f)

# Extract beats and districts
beat_district_mapping = {feature['properties']['BEAT_NUMBE']: feature['properties']['DISTRICT'] for feature in geojson_beats['features']}
beat_district_df = pd.DataFrame(list(beat_district_mapping.items()), columns=['beat', 'district'])
# Merge the beat-district mapping with the main dataframe
df_map = df_map.merge(beat_district_df, on='beat', how='left')
def determine_district_from_beat(beat):
    beat_str = str(beat)
    if len(beat_str) == 3:
        return int(beat_str[0])
    elif len(beat_str) == 4:
        return int(beat_str[:2])
    else:
        return np.nan

# Fill missing district values
df_map.loc[df_map['district'].isnull(), 'district'] = df_map.loc[df_map['district'].isnull(), 'beat'].apply(determine_district_from_beat)

# Load the neighborhoods JSON file
with open(geojson_path_neighborhoods, 'r') as f:
    district_neighborhoods = json.load(f)

# Convert district keys to strings for consistency
district_neighborhoods = {str(int(k)): v for k, v in district_neighborhoods.items()}

# Convert district values to strings without leading zeros in the DataFrame for consistency
df_map['district'] = df_map['district'].apply(lambda x: str(int(x)))

# Map neighborhoods to districts
df_map['neighborhood'] = df_map['district'].map(district_neighborhoods)

# Add the crime_category column
category_map = {
    'BATTERY': 'Violent Crimes',
    'OFFENSE INVOLVING CHILDREN': 'Crimes Against Children',
    'ROBBERY': 'Violent Crimes',
    'THEFT': 'Property Crimes',
    'CRIMINAL DAMAGE': 'Property Crimes',
    'ASSAULT': 'Violent Crimes',
    'BURGLARY': 'Property Crimes',
    'OTHER OFFENSE': 'Miscellaneous Crimes',
    'MOTOR VEHICLE THEFT': 'Property Crimes',
    'WEAPONS VIOLATION': 'Public Order Crimes',
    'STALKING': 'Violent Crimes',
    'DECEPTIVE PRACTICE': 'White Collar Crimes',
    'CRIMINAL SEXUAL ASSAULT': 'Violent Crimes',
    'CRIMINAL TRESPASS': 'Property Crimes',
    'PROSTITUTION': 'Public Order Crimes',
    'NARCOTICS': 'Drug Offenses',
    'INTERFERENCE WITH PUBLIC OFFICER': 'Miscellaneous Crimes',
    'PUBLIC PEACE VIOLATION': 'Public Order Crimes',
    'CONCEALED CARRY LICENSE VIOLATION': 'Public Order Crimes',
    'ARSON': 'Property Crimes',
    'HOMICIDE': 'Violent Crimes',
    'KIDNAPPING': 'Violent Crimes',
    'SEX OFFENSE': 'Violent Crimes',
    'INTIMIDATION': 'Violent Crimes',
    'LIQUOR LAW VIOLATION': 'Public Order Crimes',
    'OBSCENITY': 'Public Order Crimes',
    'GAMBLING': 'Public Order Crimes',
    'PUBLIC INDECENCY': 'Public Order Crimes',
    'NON-CRIMINAL': 'Miscellaneous Crimes',
    'OTHER NARCOTIC VIOLATION': 'Drug Offenses',
    'HUMAN TRAFFICKING': 'Miscellaneous Crimes',
    'CRIM SEXUAL ASSAULT': 'Miscellaneous Crimes',
    'NON-CRIMINAL (SUBJECT SPECIFIED)': 'Miscellaneous Crimes',
    'NON - CRIMINAL': 'Miscellaneous Crimes',
    'RITUALISM': 'Miscellaneous Crimes',
    'DOMESTIC VIOLENCE': 'Violent Crimes'
}
df_map['crime_category'] = df_map['primary_type'].map(category_map)

# Ensure all necessary columns are categorized correctly
for col in ['beat', 'district', 'neighborhood', 'primary_type', 'crime_category']:
    if col in df_map.columns:
        df_map[col] = df_map[col].astype('category')

# Define the columns to keep
columns_to_keep = [
    'date', 'month', 'day_of_week', 'hour', 'block', 'primary_type', 'description', 'location_description',
    'arrest', 'beat', 'district', 'year', 'updated_on', 'latitude', 'longitude',
    'neighborhood', 'crime_category'
]

# Filter the columns to include only the specified ones
df_filtered = df_map[columns_to_keep]

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(df_filtered, geometry=gpd.points_from_xy(df_filtered.longitude, df_filtered.latitude), crs='EPSG:4326')

def calculate_crime_rates(gdf, time_column, group_column):
    results = []
    crime_categories = gdf['crime_category'].unique()
    total_counts = gdf.groupby([time_column, 'crime_category']).size().reset_index(name='total_count')

    for category in crime_categories:
        category_gdf = gdf[gdf['crime_category'] == category]
        specific_counts = category_gdf.groupby([time_column, group_column, 'neighborhood']).size().reset_index(name='specific_count')
        crime_rates = pd.merge(specific_counts, total_counts[total_counts['crime_category'] == category], on=[time_column], how='left')
        crime_rates['specific_count'] = crime_rates['specific_count'].fillna(0)
        crime_rates['crime_rate'] = crime_rates['specific_count'] / crime_rates['total_count']
        crime_rates['crime_category'] = category
        results.append(crime_rates)

    final_result = pd.concat(results, ignore_index=True)
    overall_counts = gdf.groupby([time_column, group_column, 'neighborhood']).size().reset_index(name='specific_count')
    overall_total_counts = gdf.groupby([time_column]).size().reset_index(name='total_count')
    overall_counts = pd.merge(overall_counts, overall_total_counts, on=[time_column], how='left')
    overall_counts['crime_rate'] = overall_counts['specific_count'] / overall_counts['total_count']
    overall_counts['crime_category'] = 'All Crimes'
    
    final_result = pd.concat([final_result, overall_counts], ignore_index=True)
    return final_result

# Aggregation by day of the week and beat
daily_beat_agg = calculate_crime_rates(gdf, 'day_of_week', 'beat')
daily_district_agg = calculate_crime_rates(gdf, 'day_of_week', 'district')
monthly_beat_agg = calculate_crime_rates(gdf, 'month', 'beat')
monthly_district_agg = calculate_crime_rates(gdf, 'month', 'district')
hourly_beat_agg = calculate_crime_rates(gdf, 'hour', 'beat')
hourly_district_agg = calculate_crime_rates(gdf, 'hour', 'district')
yearly_beat_agg = calculate_crime_rates(gdf, 'year', 'beat')
yearly_district_agg = calculate_crime_rates(gdf, 'year', 'district')

# Save the aggregated data to CSV files
daily_beat_agg.to_csv('daily_beat_crime_rates.csv', index=False)
daily_district_agg.to_csv('daily_district_crime_rates.csv', index=False)
monthly_beat_agg.to_csv('monthly_beat_crime_rates.csv', index=False)
monthly_district_agg.to_csv('monthly_district_crime_rates.csv', index=False)
hourly_beat_agg.to_csv('hourly_beat_crime_rates.csv', index=False)
hourly_district_agg.to_csv('hourly_district_crime_rates.csv', index=False)
yearly_beat_agg.to_csv('yearly_beat_crime_rates.csv', index=False)
yearly_district_agg.to_csv('yearly_district_crime_rates.csv', index=False)
