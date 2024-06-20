"""
Map visualization.
"""

import json
from enum import Enum

import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State

from app import app
from paths import DATA_MAP_FOLDER

# FIXME slider doesn't show correctly on first load
# TODO make animation smoother


class GeoLevel(Enum):
    """
    Geo level for the data aggregation.
    """

    DISTRICT = "district"
    BEAT = "beat"

    def read_boundaries(self):
        with open(
            f"{DATA_MAP_FOLDER}/police_{self.value}s_boundaries.geojson",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    @staticmethod
    def from_str(geo_level_str):
        for geo_level in GeoLevel:
            if geo_level_str.lower() == geo_level.value:
                return geo_level

        raise ValueError(f"Invalid geo level: {geo_level_str}")


class TimeFilter(Enum):
    """
    Time filter for the data aggregation.
    """

    HOURLY = "hour"
    DAILY = "weekday"
    MONTHLY = "month"
    YEARLY = "year"

    @staticmethod
    def from_str(time_filter_str):
        for time_filter in TimeFilter:
            if time_filter_str.lower() == time_filter.value:
                return time_filter

        raise ValueError(f"Invalid time filter: {time_filter_str}")


DEFAULT_GEOLEVEL = GeoLevel.DISTRICT
DEFAULT_TIME_FILTER = TimeFilter.YEARLY


class DataAggregation:
    """
    Data aggregation of crime rates by geolevel and time_filter.
    """

    def _path(self):
        return f"{DATA_MAP_FOLDER}/{self.time_filter.value}_{self.geolevel.value}_crime_rates.csv"

    def __init__(self, geolevel: GeoLevel, time_filter: TimeFilter):
        self.geolevel = geolevel
        self.time_filter = time_filter
        self.csv = pd.read_csv(self._path())
        if geolevel == GeoLevel.BEAT:
            self.csv["beat"] = self.csv["beat"].apply(lambda x: str(x).zfill(4))
        self.csv["crime_rate"] = (self.csv["crime_rate"] * 100).round(2)
        self.max_crime_rate = (
            self.csv.groupby("crime_category")["crime_rate"].max().to_dict()
        )
        self.csv["crime_category_lower"] = self.csv["crime_category"].str.lower()


AGGREGATIONS = {
    (geolevel, time_filter): DataAggregation(geolevel, time_filter)
    for geolevel in GeoLevel
    for time_filter in TimeFilter
}


GEOJSONS = {geolevel: GeoLevel(geolevel).read_boundaries() for geolevel in GeoLevel}

HOURS = list(range(24))

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

MONTHS = [
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

# Extract unique years, months, days, hours, and crime categories
YEARS = sorted(
    AGGREGATIONS[(GeoLevel.DISTRICT, TimeFilter.YEARLY)].csv["year"].unique()
)

CRIMES = sorted(
    AGGREGATIONS[(GeoLevel.DISTRICT, TimeFilter.YEARLY)].csv["crime_category"].unique()
)


def convert_to_12_hour(hour):
    """
    Convert 24-hour format to 12-hour format with AM/PM.
    """
    hour = int(hour)
    if hour == 0:
        return "12 AM"
    elif hour == 12:
        return "12 PM"
    elif hour > 12:
        return f"{hour - 12} PM"
    else:
        return f"{hour} AM"


time_filter_values = {
    TimeFilter.HOURLY: HOURS,
    TimeFilter.DAILY: WEEKDAYS,
    TimeFilter.MONTHLY: MONTHS,
    TimeFilter.YEARLY: YEARS,
}


def create_choropleth(crime_category, selected_time_idx, time_filter_str, geolevel_str):
    """
    Create a choropleth map.

    Args:
        crime_category: The crime category.
        time_value: The time value.
        time_filter: The time filter.
        geolevel: The geolevel.

    Returns:
        The choropleth map.
    """
    time_filter = TimeFilter.from_str(time_filter_str)
    geolevel = GeoLevel.from_str(geolevel_str)
    time_value = time_filter_values[time_filter][selected_time_idx]
    aggregation = AGGREGATIONS[(geolevel, time_filter)]
    filtered_data = aggregation.csv[
        (aggregation.csv[time_filter.value] == time_value)
        & (aggregation.csv["crime_category"] == crime_category)
    ]
    max_crime_rate = aggregation.max_crime_rate[crime_category]
    geojson = GEOJSONS[geolevel]
    feature_id = (
        "properties.dist_num"
        if geolevel == GeoLevel.DISTRICT
        else "properties.beat_num"
    )

    hover_template = (
        f"<b>{geolevel.value.capitalize()}:</b> %{{location}}<br>"
        + "<b>Neighborhood:</b> %{customdata[0]}<br>"
        + "<b>Crime Count:</b> %{customdata[1]:,} in %{customdata[2]:,}"
        + " of %{customdata[3]} that occurred "
        + (
            "on"
            if time_filter == time_filter.DAILY
            else "at" if time_filter == time_filter.HOURLY else "in"
        )
        + " %{customdata[4]}<br>"
        + "<b>Crime Rate:</b> %{z}%<br>"
    )

    custom_data = filtered_data[
        [
            "neighborhood",
            "specific_count",
            "total_count",
            "crime_category_lower",
            time_filter.value,
        ]
    ].values

    fig = go.Figure(
        go.Choropleth(
            geojson=geojson,
            locations=filtered_data[geolevel.value],
            z=filtered_data["crime_rate"],
            featureidkey=feature_id,
            colorscale="Plasma",
            zmin=0,
            zmax=max_crime_rate,
            colorbar_title="Crime Rate (%)",
            hovertemplate=hover_template,
            customdata=custom_data,
        )
    )
    time_str = (
        convert_to_12_hour(time_value)
        if time_filter == time_filter.HOURLY
        else time_value
    )
    fig.update_layout(
        title=f"Crime Rate by {geolevel} in Chicago - {crime_category} ({time_str})",
        geo={"fitbounds": "locations", "visible": False},
        coloraxis_colorbar={"title": "Crime Rate (%)"},
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        height=600,
        font={"family": "Oswald"},
    )

    return fig


def get_html(figure):
    return html.Div(
        className="map-container",
        children=[
            dcc.Graph(
                className="map",
                id="choropleth",
                config={"displayModeBar": False},
                figure=figure,
            ),
            html.Div(
                className="map-params",
                children=[
                    html.H2("Parameters"),
                    html.Div(
                        className="map-dropdowns",
                        children=[
                            html.H4("Geographical Level"),
                            dcc.Dropdown(
                                id="geo-level-dropdown",
                                options=[
                                    {"label": "Beat", "value": "beat"},
                                    {"label": "District", "value": "district"},
                                ],
                                value="district",
                                clearable=False,
                                style={"width": "100%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className="map-dropdowns",
                        children=[
                            html.H4("Time Filter"),
                            dcc.Dropdown(
                                id="time-filter-dropdown",
                                options=[
                                    {"label": "Hourly", "value": "hour"},
                                    {"label": "Daily", "value": "weekday"},
                                    {"label": "Monthly", "value": "month"},
                                    {"label": "Yearly", "value": "year"},
                                ],
                                value="year",
                                clearable=False,
                                style={"width": "100%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className="map-dropdowns",
                        children=[
                            html.H4("Crime Category"),
                            dcc.Dropdown(
                                id="crime-category-dropdown",
                                options=[
                                    {"label": category, "value": category}
                                    for category in CRIMES
                                ],
                                value=CRIMES[0],
                                clearable=False,
                                style={"width": "100%"},
                            ),
                        ],
                    ),
                    html.Div(
                        [
                            dcc.Slider(
                                id="time-slider",
                                min=0,
                                max=len(YEARS) - 1,
                                value=0,
                                marks={i: str(year) for i, year in enumerate(YEARS)},
                                step=None,
                                updatemode="drag",
                            )
                        ],
                        style={"width": "100%", "padding": "0px 20px 20px 20px"},
                    ),
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
                ],
            ),
        ],
    )


def get_figure(_data):
    return create_choropleth(
        CRIMES[0], 0, DEFAULT_TIME_FILTER.value, DEFAULT_GEOLEVEL.value
    )


def get_hover_template():
    return "No data to show"


@app.callback(
    Output("choropleth", "figure"),
    [
        Input("crime-category-dropdown", "value"),
        Input("time-slider", "value"),
        Input("time-filter-dropdown", "value"),
        Input("geo-level-dropdown", "value"),
    ],
)
def update_map(crime_category, selected_time_idx, time_filter_str, geolevel_str):
    return create_choropleth(
        crime_category, selected_time_idx, time_filter_str, geolevel_str
    )


SCALES_LENGTHS = {
    "hour": len(HOURS),
    "weekday": len(WEEKDAYS),
    "month": len(MONTHS),
    "year": len(YEARS),
}

SCALES_MARKS = {
    "hour": {i: convert_to_12_hour(hour) for i, hour in enumerate(HOURS)},
    "weekday": {i: day for i, day in enumerate(WEEKDAYS)},
    "month": {i: month for i, month in enumerate(MONTHS)},
    "year": {i: str(year) for i, year in enumerate(YEARS)},
}


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
    _geo_level,
    _play_clicks,
    _pause_clicks,
    _n_intervals,
    interval_disabled,
    current_value,
):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    scale_length = SCALES_LENGTHS[time_filter]

    if trigger_id in ["time-filter-dropdown", "geo-level-dropdown"]:
        return scale_length - 1, SCALES_MARKS[time_filter], 0, True

    if trigger_id == "play-button":
        interval_disabled = False
    elif trigger_id == "pause-button":
        interval_disabled = True
    elif trigger_id == "interval-component" and not interval_disabled:
        current_value = (current_value + 1) % scale_length

    return (
        (scale_length - 1,),
        (SCALES_MARKS[time_filter],),
        current_value,
        interval_disabled,
    )
