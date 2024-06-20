"""
Histogram visualization.
"""

from enum import Enum

import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output

from app import app
from viz.paths import DATA_HISTOGRAM_FOLDER


class TimeFilter:
    """
    Data class for time filters csvs.
    """

    def __init__(self, name):
        self.csv = pd.read_csv(f"{DATA_HISTOGRAM_FOLDER}/histogram_{name}.csv")


class TimeFilters(Enum):
    """
    Enum for time filters.
    """

    TIME_OF_DAY = TimeFilter("time_of_day")
    DAY = TimeFilter("day")
    MONTH = TimeFilter("month")


def time_filters_from_name(name) -> TimeFilters:
    name = name.lower()
    if name == "time_of_day":
        return TimeFilters.TIME_OF_DAY
    if name == "day":
        return TimeFilters.DAY
    if name == "month":
        return TimeFilters.MONTH

    raise ValueError(f"Unknown time filter: {name}")


CRIME_TYPES = [ct.capitalize() for ct in TimeFilters.TIME_OF_DAY.value.csv.columns[1:]]
DEFAULT_CRIME_TYPE = "Total"


def create_histogram(time_filter: TimeFilters, crime_type):
    # Create the figure
    fig = go.Figure()

    # Add traces
    fig.add_trace(
        go.Bar(
            x=time_filter.value.csv[time_filter.name.lower()],
            y=time_filter.value.csv[crime_type.upper()],
            name="main",
            visible=True,
        )
    )

    # Set layout
    fig.update_layout(
        title="Crimes in time",
        xaxis_title=f"{time_filter.name.capitalize()}s",
        yaxis_title=f"{crime_type} count",
        barmode="group",
        title_x=0.5,
    )

    return fig


def get_figure(_data):
    fig = create_histogram(TimeFilters.MONTH, DEFAULT_CRIME_TYPE)
    return fig


def get_hover_template():
    """
    When hovering over a bar, display the count of crimes.
    """
    return "Count: %{y}"


def get_html(figure):
    """
    Returns the HTML element to be displayed.

    Args:
        figure: The figure to display
    Returns:
        The HTML element to display.
    """
    return html.Div(
        className="histogram-container",
        children=[
            dcc.Graph(
                className="histogram",
                id="histogram",
                figure=figure,
                config={"displayModeBar": False},
            ),
            html.Div(
                className="histogram-params",
                children=[
                    html.H2("Parameters"),
                    html.Div(
                        className="histogram-dropdowns",
                        children=[
                            html.H4("Time scale"),
                            dcc.Dropdown(
                                id="histogram-time-filter-dropdown",
                                options=[
                                    {"label": "Times of day", "value": "time_of_day"},
                                    {"label": "Days", "value": "day"},
                                    {"label": "Months", "value": "month"},
                                ],
                                value="time_of_day",
                                clearable=False,
                                style={"width": "100%"},
                            ),
                            html.H4("Crime type"),
                            dcc.Dropdown(
                                id="crime-type-dropdown",
                                options=[
                                    {"label": crime_type, "value": crime_type}
                                    for crime_type in CRIME_TYPES
                                ],
                                value=DEFAULT_CRIME_TYPE,
                                clearable=False,
                                style={"width": "100%"},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


@app.callback(
    Output("histogram", "figure"),
    [
        Input("histogram-time-filter-dropdown", "value"),
        Input("crime-type-dropdown", "value"),
    ],
)
def histogram_callback(time_filter, crime_type):
    time_filter = time_filters_from_name(time_filter)
    return create_histogram(time_filter, crime_type)
