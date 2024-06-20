"""
Multiline chart visualization.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output

from app import app


def process_data(data):
    """
    Process the data for the visualization.

    Args:
        data: The data to process.
    Returns:
        The processed data.
    """
    total_crimes = data.shape[0]
    # Convert data to datetime, get year and group by year and primary type
    data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y %I:%M:%S %p")
    data["Year"] = data["Date"].dt.year
    data = data.groupby(["Year", "Primary Type"]).size().reset_index(name="Annual")

    # Complete with 0 for the years that don't have data
    for year in data["Year"].unique():
        for primary_type in data["Primary Type"].unique():
            if primary_type not in data[data["Year"] == year]["Primary Type"].values:
                data = pd.concat(
                    [
                        data,
                        pd.DataFrame(
                            {
                                "Year": [year],
                                "Primary Type": [primary_type],
                                "Annual": [0],
                            }
                        ),
                    ]
                )

    # Annual the number of crimes per primary type
    annual_crimes = data.groupby(["Primary Type"]).sum().reset_index()
    annual_crimes = annual_crimes.sort_values(by="Annual", ascending=False)
    annual_crimes = annual_crimes.drop(columns=["Year"])

    # Get the crimes that represent 95% of the total
    annual_crimes["Cumulative"] = annual_crimes["Annual"].cumsum() / total_crimes
    annual_crimes = annual_crimes[annual_crimes["Cumulative"] <= 0.95]

    # Calculate the number of crimes that are not in the top 95%
    other_offense = data[~data["Primary Type"].isin(annual_crimes["Primary Type"])]
    other_offense = other_offense.groupby("Year").sum().reset_index()
    other_offense["Primary Type"] = "OTHER OFFENSE"

    # Append the other offenses to the data
    data = data[data["Primary Type"].isin(annual_crimes["Primary Type"])]
    if "OTHER OFFENSE" in data["Primary Type"].unique():
        data.loc[data["Primary Type"] == "OTHER OFFENSE", "Annual"] += other_offense[
            "Annual"
        ].values
    else:
        data = data.append(other_offense, ignore_index=True)

    # Get the cumulative sum
    data["Cumulative"] = data.groupby("Primary Type")["Annual"].cumsum()

    assert total_crimes == data["Annual"].sum()

    return data


def get_hover_template(mode):
    """
    Returns the hover template for the figure.

    Returns:
        The hover template.
    """
    if mode == "Cumulative":
        return "<b>%{customdata[1]}</b><br>%{y} total crimes from 2001 to %{x}<extra></extra>"
    else:
        return "<b>%{customdata[1]}</b><br>%{y} crimes in %{x}<extra></extra>"


def get_figure(data):
    """
    Returns a plotly figure object

    Args:
        data: The data to display
    Returns:
        The figure to be displayed.
    """
    data = process_data(data)

    # Add traces for Annual
    fig = px.line(
        data,
        x="Year",
        y="Annual",
        color="Primary Type",
        title="Number of crimes per year",
    )
    fig.update_traces(hovertemplate=get_hover_template("Annual"))
    for trace in fig.data:
        trace.customdata = np.stack(
            [np.full(len(trace.y), "Annual"), np.full(len(trace.y), trace.name)],
            axis=-1,
        )

    # Add traces for Cumulative
    for primary_type in data["Primary Type"].unique():
        df = data[data["Primary Type"] == primary_type]
        customdata = np.stack(
            [np.full(len(df), "Cumulative"), np.full(len(df), primary_type)], axis=-1
        )
        fig.add_trace(
            go.Scatter(
                x=df["Year"],
                y=df["Cumulative"],
                mode="lines",
                visible=False,
                name=primary_type,
                hovertemplate=get_hover_template("Cumulative"),
                customdata=customdata,
                legendgroup=primary_type,
            )
        )

    # Update layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of crimes",
        legend_title="Primary Type",
        title_x=0.5,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True),
    )

    # Get the maximum value for the shapes
    max_annual, max_cumulative = 0, 0
    for trace in fig.data:
        if trace.customdata[0][0] == "Annual":
            max_annual = max(max_annual, trace.y.all())
        else:
            max_cumulative = max(max_cumulative, trace.y.all())

    # 2008 crisis
    crisis_shape = dict(
        type="rect",
        x0=2007,
        x1=2010,
        y0=0,
        y1=max_annual,
        fillcolor="red",
        opacity=0.3,
        line_width=0,
        line=dict(width=0),
        name="economic",
        visible=False,
    )
    crisis_annotation = dict(
        x=2008,  # Position x de l'annotation
        y=max_annual,  # Position y de l'annotation
        text="2008 Economic Crisis",  # Texte de l'annotation
        showarrow=True,  # Pas de flèche
        font=dict(color="red", size=12),  # Style du texte
        bgcolor="rgba(255,0,0,0.2)",  # Couleur de fond
        xanchor="center",  # Ancrage horizontal au centre
        visible=False,
    )

    # Covid
    covid_shape = dict(
        type="rect",
        x0=2019,
        x1=2022,
        y0=0,
        y1=max_annual,
        fillcolor="orange",
        opacity=0.3,
        line_width=0,
        line=dict(width=0),
        name="covid",
        visible=False,
    )
    covid_annotation = dict(
        x=2021,  # Position x de l'annotation
        y=max_annual,  # Position y de l'annotation
        text="Covid-19 Pandemic",  # Texte de l'annotation
        showarrow=True,  # Pas de flèche
        font=dict(color="orange", size=12),  # Style du texte
        bgcolor="rgba(255,165,0,0.2)",  # Couleur de fond
        xanchor="center",  # Ancrage horizontal au centre
        visible=False,
    )

    # Add shapes to the layout
    fig.update_layout(shapes=[crisis_shape, covid_shape])
    fig.update_layout(annotations=[crisis_annotation, covid_annotation])

    return fig


# TODO create premade components for buttons and containers, to unify all visualization


def get_html(figure):
    return html.Div(
        className="multiline-container",
        children=[
            dcc.Graph(
                className="multiline-graph",
                id="multiline-graph",
                figure=figure,
                config={"displayModeBar": False},
            ),
            html.Div(
                className="multiline-params",
                children=[
                    html.H2("Parameters"),
                    html.Div(
                        className="multiline-buttons",
                        children=[
                            html.H4("Display mode"),
                            dcc.Dropdown(
                                className="multiline-mode",
                                id="multiline-mode",
                                options=[
                                    {"label": "Annual", "value": "Annual"},
                                    {
                                        "label": "Cumulative",
                                        "value": "Cumulative",
                                    },
                                ],
                                value="Annual",
                                clearable=False,
                                style={"width": "100%"},
                            ),
                            html.H4("Crisis"),
                            dcc.Checklist(
                                className="multiline-checklist",
                                id="multiline-checklist",
                                options=[
                                    {
                                        "label": "2008 crisis",
                                        "value": "2008",
                                    },
                                    {
                                        "label": "Covid crisis",
                                        "value": "covid",
                                    },
                                ],
                                value=[],
                                labelStyle={
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center",
                                    "flex-direction": "row",
                                    "width": "100%",
                                },
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


@app.callback(
    Output("multiline-graph", "figure"),
    [
        Input("multiline-graph", "figure"),
        Input("multiline-mode", "value"),
        Input("multiline-checklist", "value"),
    ],
)
def multiline_update_mode(multiline_graph, display_mode, checklist_values):
    max_y = 0
    # Update the traces visibility
    for trace in multiline_graph["data"]:
        if trace.get("customdata")[0][0] == display_mode:
            max_y = max(max_y, max(trace["y"]))
            trace["visible"] = True
        else:
            trace["visible"] = False

    # Update the 2008 crisis shape and annotation
    if "2008" in checklist_values:
        multiline_graph["layout"]["shapes"][0]["visible"] = True
        multiline_graph["layout"]["annotations"][0]["visible"] = True
    else:
        multiline_graph["layout"]["shapes"][0]["visible"] = False
        multiline_graph["layout"]["annotations"][0]["visible"] = False

    # Update the covid crisis shape
    if "covid" in checklist_values:
        multiline_graph["layout"]["shapes"][1]["visible"] = True
        multiline_graph["layout"]["annotations"][1]["visible"] = True
    else:
        multiline_graph["layout"]["shapes"][1]["visible"] = False
        multiline_graph["layout"]["annotations"][1]["visible"] = False

    # Update the max y value
    multiline_graph["layout"]["shapes"][0]["y1"] = max_y
    multiline_graph["layout"]["annotations"][0]["y"] = max_y
    multiline_graph["layout"]["shapes"][1]["y1"] = max_y
    multiline_graph["layout"]["annotations"][1]["y"] = max_y

    return multiline_graph
