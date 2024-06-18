# -*- coding: utf-8 -*-
"""
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file contains the source code for project.
"""

import dash
import dash_html_components as html
import importlib
import dash_core_components as dcc
import os
from dash.dependencies import Input, Output, State

import pandas as pd

app = dash.Dash(__name__)
app.title = "Chicago Crimes | INF8808"

# DATA_PATH = "assets/data/crimes.csv" # full dataset
DATA_PATH = "assets/data/crimes_reduced.csv"  # 1000 times reduced dataset

with open(DATA_PATH, encoding="utf-8") as data_file:
    data = pd.read_csv(data_file)

# Load figures
figures_files = [
    os.path.splitext(f)[0]
    for f in os.listdir("viz")
    if f.endswith(".py") and not f.startswith("viz_template")
]
figures = {}

for figure_file in figures_files:
    module = importlib.import_module(f"viz.{figure_file}")
    figures[figure_file] = module.get_figure(data)

app.layout = html.Div(
    className="content",
    children=[
        html.Header(
            children=[
                html.H1(
                    "Spatial and temporal analyses of Chicago criminals trends since 2001"
                ),
                html.H2("How did crime evolve since 2001 in Chicago ?"),
            ]
        ),
        html.Main(
            className="viz-container",
            # Our visualizations will be displayed here
            children=[
                # ------ Multiline graph ------
                html.Div(
                    className="multiline-container",
                    children=[
                        dcc.Graph(
                            className="multiline-graph",
                            id="multiline-graph",
                            figure=figures["multiline"],
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
                ),
                # ------ End of Multiline graph ------
            ],
        ),
    ],
)


# ------ Multiline graph callback ------
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
