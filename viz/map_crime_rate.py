"""
Map visualization.
"""

import json

import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Load the crime data
monthly_district_file_path = "monthly_district_crime_rates.csv"
yearly_district_file_path = "yearly_district_crime_rates.csv"
daily_district_file_path = "daily_district_crime_rates.csv"
hourly_district_file_path = "hourly_district_crime_rates.csv"

monthly_beat_file_path = "monthly_beat_crime_rates.csv"
yearly_beat_file_path = "yearly_beat_crime_rates.csv"
daily_beat_file_path = "daily_beat_crime_rates.csv"
hourly_beat_file_path = "hourly_beat_crime_rates.csv"

monthly_district_data = pd.read_csv(monthly_district_file_path)
yearly_district_data = pd.read_csv(yearly_district_file_path)
daily_district_data = pd.read_csv(daily_district_file_path)
hourly_district_data = pd.read_csv(hourly_district_file_path)

monthly_beat_data = pd.read_csv(monthly_beat_file_path)
yearly_beat_data = pd.read_csv(yearly_beat_file_path)
daily_beat_data = pd.read_csv(daily_beat_file_path)
hourly_beat_data = pd.read_csv(hourly_beat_file_path)

# Convert beat values to strings with leading zeros
monthly_beat_data["beat"] = monthly_beat_data["beat"].apply(lambda x: str(x).zfill(4))
yearly_beat_data["beat"] = yearly_beat_data["beat"].apply(lambda x: str(x).zfill(4))
daily_beat_data["beat"] = daily_beat_data["beat"].apply(lambda x: str(x).zfill(4))
hourly_beat_data["beat"] = hourly_beat_data["beat"].apply(lambda x: str(x).zfill(4))


# Load the GeoJSON files for police district and beat boundaries
district_geojson_path = "Boundaries - Police Districts (current).geojson"
with open(district_geojson_path) as f:
    district_geojson = json.load(f)

beat_geojson_path = "Boundaries - Police Beats (current).geojson"
with open(beat_geojson_path) as f:
    beat_geojson = json.load(f)

# Extract unique years, months, days, hours, and crime categories
years = sorted(yearly_district_data["year"].unique())
month_order = [
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
]
months = [
    month for month in month_order if month in monthly_district_data["month"].unique()
]
days_of_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
hours = sorted(hourly_district_data["hour"].unique())
crime_categories = sorted(yearly_district_data["crime_category"].unique())

# Ensure same order for beat data
months_beats = [
    month for month in month_order if month in monthly_beat_data["month"].unique()
]
days_of_week_beats = [
    day for day in days_of_week if day in daily_beat_data["day_of_week"].unique()
]

# Update the crime rate to percentage in all datasets
monthly_district_data["crime_rate"] = (monthly_district_data["crime_rate"] * 100).round(
    2
)
yearly_district_data["crime_rate"] = (yearly_district_data["crime_rate"] * 100).round(2)
daily_district_data["crime_rate"] = (daily_district_data["crime_rate"] * 100).round(2)
hourly_district_data["crime_rate"] = (hourly_district_data["crime_rate"] * 100).round(2)

monthly_beat_data["crime_rate"] = (monthly_beat_data["crime_rate"] * 100).round(2)
yearly_beat_data["crime_rate"] = (yearly_beat_data["crime_rate"] * 100).round(2)
daily_beat_data["crime_rate"] = (daily_beat_data["crime_rate"] * 100).round(2)
hourly_beat_data["crime_rate"] = (hourly_beat_data["crime_rate"] * 100).round(2)

# Calculate max crime rate for each crime category in all datasets
monthly_max_crime_rates_district = (
    monthly_district_data.groupby("crime_category")["crime_rate"].max().to_dict()
)
yearly_max_crime_rates_district = (
    yearly_district_data.groupby("crime_category")["crime_rate"].max().to_dict()
)
daily_max_crime_rates_district = (
    daily_district_data.groupby("crime_category")["crime_rate"].max().to_dict()
)
hourly_max_crime_rates_district = (
    hourly_district_data.groupby("crime_category")["crime_rate"].max().to_dict()
)

monthly_max_crime_rates_beat = (
    monthly_beat_data.groupby("crime_category")["crime_rate"].max().to_dict()
)
yearly_max_crime_rates_beat = (
    yearly_beat_data.groupby("crime_category")["crime_rate"].max().to_dict()
)
daily_max_crime_rates_beat = (
    daily_beat_data.groupby("crime_category")["crime_rate"].max().to_dict()
)
hourly_max_crime_rates_beat = (
    hourly_beat_data.groupby("crime_category")["crime_rate"].max().to_dict()
)


# Function to convert 24-hour format to 12-hour format with AM/PM
def convert_to_12_hour(hour):
    hour = int(hour)
    if hour == 0:
        return "12 AM"
    elif hour == 12:
        return "12 PM"
    elif hour > 12:
        return f"{hour - 12} PM"
    else:
        return f"{hour} AM"


# Add a lowercase crime category column
for data in [
    monthly_district_data,
    yearly_district_data,
    daily_district_data,
    hourly_district_data,
    monthly_beat_data,
    yearly_beat_data,
    daily_beat_data,
    hourly_beat_data,
]:
    data["crime_category_lower"] = data["crime_category"].str.lower()


# Function to create the choropleth map
def create_choropleth(crime_category, time_value, time_filter, geo_level):
    label = "District" if geo_level == "District" else "Beat"
    if geo_level == "District":
        if time_filter == "Monthly":
            filtered_data = monthly_district_data[
                (monthly_district_data["month"] == time_value)
                & (monthly_district_data["crime_category"] == crime_category)
            ]
            max_crime_rate = monthly_max_crime_rates_district[crime_category]
            geojson = district_geojson
            feature_id = "properties.dist_num"
        elif time_filter == "Yearly":
            filtered_data = yearly_district_data[
                (yearly_district_data["year"] == time_value)
                & (yearly_district_data["crime_category"] == crime_category)
            ]
            max_crime_rate = yearly_max_crime_rates_district[crime_category]
            geojson = district_geojson
            feature_id = "properties.dist_num"
        elif time_filter == "Daily":
            filtered_data = daily_district_data[
                (daily_district_data["day_of_week"] == time_value)
                & (daily_district_data["crime_category"] == crime_category)
            ]
            max_crime_rate = daily_max_crime_rates_district[crime_category]
            geojson = district_geojson
            feature_id = "properties.dist_num"
        else:  # Hourly
            filtered_data = hourly_district_data[
                (hourly_district_data["hour"] == time_value)
                & (hourly_district_data["crime_category"] == crime_category)
            ]
            filtered_data["time_display"] = filtered_data["hour"].apply(
                convert_to_12_hour
            )
            max_crime_rate = hourly_max_crime_rates_district[crime_category]
            geojson = district_geojson
            feature_id = "properties.dist_num"
    else:  # Beat
        if time_filter == "Monthly":
            filtered_data = monthly_beat_data[
                (monthly_beat_data["month"] == time_value)
                & (monthly_beat_data["crime_category"] == crime_category)
            ]
            max_crime_rate = monthly_max_crime_rates_beat[crime_category]
            geojson = beat_geojson
            feature_id = "properties.beat_num"
        elif time_filter == "Yearly":
            filtered_data = yearly_beat_data[
                (yearly_beat_data["year"] == time_value)
                & (yearly_beat_data["crime_category"] == crime_category)
            ]
            max_crime_rate = yearly_max_crime_rates_beat[crime_category]
            geojson = beat_geojson
            feature_id = "properties.beat_num"
        elif time_filter == "Daily":
            filtered_data = daily_beat_data[
                (daily_beat_data["day_of_week"] == time_value)
                & (daily_beat_data["crime_category"] == crime_category)
            ]
            max_crime_rate = daily_max_crime_rates_beat[crime_category]
            geojson = beat_geojson
            feature_id = "properties.beat_num"
        else:  # Hourly
            filtered_data = hourly_beat_data[
                (hourly_beat_data["hour"] == time_value)
                & (hourly_beat_data["crime_category"] == crime_category)
            ]
            filtered_data["time_display"] = filtered_data["hour"].apply(
                convert_to_12_hour
            )
            max_crime_rate = hourly_max_crime_rates_beat[crime_category]
            geojson = beat_geojson
            feature_id = "properties.beat_num"

    hover_template = (
        f"<b>{label}:</b> %{{location}}<br>"
        + "<b>Neighborhood:</b> %{customdata[0]}<br>"
        + "<b>Crime Count:</b> %{customdata[1]:,} in %{customdata[2]:,} of %{customdata[3]} that occurred "
        + (
            "on"
            if time_filter == "Daily"
            else "at" if time_filter == "Hourly" else "in"
        )
        + " %{customdata[4]}<br>"
        + "<b>Crime Rate:</b> %{z}%<br>"
    )

    customdata = filtered_data[
        [
            "neighborhood",
            "specific_count",
            "total_count",
            "crime_category_lower",
            (
                "time_display"
                if time_filter == "Hourly"
                else (
                    "day_of_week"
                    if time_filter == "Daily"
                    else ("month" if time_filter == "Monthly" else "year")
                )
            ),
        ]
    ].values

    fig = go.Figure(
        go.Choropleth(
            geojson=geojson,
            locations=filtered_data["district" if geo_level == "District" else "beat"],
            z=filtered_data["crime_rate"],
            featureidkey=feature_id,
            colorscale="Plasma",
            zmin=0,
            zmax=max_crime_rate,
            colorbar_title="Crime Rate (%)",
            hovertemplate=hover_template,
            customdata=customdata,
        )
    )
    fig.update_layout(
        title=f'Crime Rate by {geo_level} in Chicago - {crime_category} ({convert_to_12_hour(time_value) if time_filter == "Hourly" else time_value})',
        geo=dict(fitbounds="locations", visible=False),
        coloraxis_colorbar=dict(title="Crime Rate (%)"),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        height=600,
        font=dict(family="Oswald"),
    )
    return fig


app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Dropdown(
                    id="geo-level-dropdown",
                    options=[
                        {"label": "District", "value": "District"},
                        {"label": "Beat", "value": "Beat"},
                    ],
                    value="District",
                    clearable=False,
                )
            ],
            style={"width": "50%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="time-filter-dropdown",
                    options=[
                        {"label": "Yearly", "value": "Yearly"},
                        {"label": "Monthly", "value": "Monthly"},
                        {"label": "Daily", "value": "Daily"},
                        {"label": "Hourly", "value": "Hourly"},
                    ],
                    value="Yearly",
                    clearable=False,
                )
            ],
            style={"width": "50%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="crime-category-dropdown",
                    options=[
                        {"label": category, "value": category}
                        for category in crime_categories
                    ],
                    value=crime_categories[0],
                    clearable=False,
                )
            ],
            style={"width": "100%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.Slider(
                    id="time-slider",
                    min=0,
                    max=len(years) - 1,
                    value=0,
                    marks={i: str(year) for i, year in enumerate(years)},
                    step=None,
                    updatemode="drag",
                )
            ],
            style={"width": "100%", "padding": "0px 20px 20px 20px"},
        ),
        dcc.Graph(id="choropleth"),
        html.Div(
            [
                dcc.Interval(
                    id="interval-component",
                    interval=2000,  # in milliseconds
                    n_intervals=0,
                    disabled=True,  # start with the interval component disabled
                ),
                html.Button("Play", id="play-button", n_clicks=0),
                html.Button("Pause", id="pause-button", n_clicks=0),
            ],
            style={"textAlign": "center"},
        ),
    ]
)


@app.callback(
    [
        Output("time-slider", "max"),
        Output("time-slider", "marks"),
        Output("time-slider", "value"),
        Output("interval-component", "disabled"),
    ],
    [
        Input("time-filter-dropdown", "value"),
        Input("geo-level-dropdown", "value"),
        Input("play-button", "n_clicks"),
        Input("pause-button", "n_clicks"),
        Input("interval-component", "n_intervals"),
    ],
    [State("interval-component", "disabled"), State("time-slider", "value")],
)
def update_time_slider_and_control_animation(
    time_filter,
    geo_level,
    play_clicks,
    pause_clicks,
    n_intervals,
    interval_disabled,
    current_value,
):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "time-filter-dropdown" or trigger_id == "geo-level-dropdown":
        if time_filter == "Monthly":
            return (
                len(months) - 1,
                {i: month for i, month in enumerate(months)},
                0,
                True,
            )
        elif time_filter == "Daily":
            return (
                len(days_of_week) - 1,
                {i: day for i, day in enumerate(days_of_week)},
                0,
                True,
            )
        elif time_filter == "Hourly":
            return (
                len(hours) - 1,
                {i: convert_to_12_hour(hour) for i, hour in enumerate(hours)},
                0,
                True,
            )
        else:
            return (
                len(years) - 1,
                {i: str(year) for i, year in enumerate(years)},
                0,
                True,
            )

    if trigger_id == "play-button":
        interval_disabled = False
    elif trigger_id == "pause-button":
        interval_disabled = True
    elif trigger_id == "interval-component" and not interval_disabled:
        if time_filter == "Monthly":
            if current_value < len(months) - 1:
                current_value += 1
            else:
                current_value = 0  # loop back to the beginning
        elif time_filter == "Daily":
            if current_value < len(days_of_week) - 1:
                current_value += 1
            else:
                current_value = 0  # loop back to the beginning
        elif time_filter == "Hourly":
            if current_value < len(hours) - 1:
                current_value += 1
            else:
                current_value = 0  # loop back to the beginning
        else:
            if current_value < len(years) - 1:
                current_value += 1
            else:
                current_value = 0  # loop back to the beginning

    return (
        (
            len(months) - 1
            if time_filter == "Monthly"
            else (
                len(days_of_week) - 1
                if time_filter == "Daily"
                else (len(hours) - 1 if time_filter == "Hourly" else len(years) - 1)
            )
        ),
        (
            {i: month for i, month in enumerate(months)}
            if time_filter == "Monthly"
            else (
                {i: day for i, day in enumerate(days_of_week)}
                if time_filter == "Daily"
                else (
                    {i: convert_to_12_hour(hour) for i, hour in enumerate(hours)}
                    if time_filter == "Hourly"
                    else {i: str(year) for i, year in enumerate(years)}
                )
            )
        ),
        current_value,
        interval_disabled,
    )


@app.callback(
    Output("choropleth", "figure"),
    [
        Input("crime-category-dropdown", "value"),
        Input("time-slider", "value"),
        Input("time-filter-dropdown", "value"),
        Input("geo-level-dropdown", "value"),
    ],
)
def update_figure(selected_category, selected_time_idx, time_filter, geo_level):
    if time_filter == "Monthly":
        time_value = months[selected_time_idx]
    elif time_filter == "Daily":
        time_value = days_of_week[selected_time_idx]
    elif time_filter == "Hourly":
        time_value = hours[selected_time_idx]
        time_value_display = convert_to_12_hour(time_value)
    else:
        time_value = years[selected_time_idx]
        time_value_display = time_value
    return create_choropleth(selected_category, time_value, time_filter, geo_level)


def get_figure(_data):
    """
    Returns a plotly figure object

    Args:
        data: The data to display
    Returns:
        The figure to be displayed.
    """
    fig = go.Figure()
    return fig


def get_hover_template():
    """
    Returns the hover template for the figure.

    Returns:
        The hover template.
    """
    return "No data to show"
