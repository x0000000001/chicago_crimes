# -*- coding: utf-8 -*-
"""
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file contains the source code for project.
"""

import importlib
import os

import dash
import pandas as pd
from dash import html

# from viz import map_crime_rate, beat_crime_type

app = dash.Dash(__name__)
app.title = "Chicago Crimes | INF8808"

# DATA_PATH = "assets/data/crimes.csv" # full dataset
DATA_PATH = "assets/data/crimes_reduced.csv"  # 1000 times reduced dataset

with open(DATA_PATH, encoding="utf-8") as data_file:
    data = pd.read_csv(data_file)

# non_visualization_files = ["viz_template.py", "paths.py", "__init__.py"]

# # Load figures
# figures_files = [
#     os.path.splitext(f)[0]
#     for f in os.listdir("viz")
#     if f.endswith(".py") and f not in non_visualization_files
# ]

visualization_files = ["multiline.py", "histogram.py"]

# Load figures
figures_files = [
    os.path.splitext(f)[0] for f in os.listdir("viz") if f in visualization_files
]

figures = {}
html_elements = []

for figure_file in figures_files:
    module = importlib.import_module(f"viz.{figure_file}")
    figures[figure_file] = figure = module.get_figure(data)
    html_elements.append(module.get_html(figure))

app.layout = html.Div(
    className="content",
    children=[
        html.Header(
            children=[
                html.H1(
                    "Spatial and temporal analyses of Chicago criminals trends since 2001"
                ),
                html.H2("How did crime evolve since 2001 in Chicago ?"),
                html.Main(
                    className="viz-container",
                    # Our visualizations will be displayed here
                    children=html_elements,
                ),
            ]
        ),
    ],
)


############################################
# CALLBACKS
############################################


# ------ Multiline graph callbacks ------


# # ------ Map callbacks ------


# @app.callback(
#     Output("choropleth", "figure"),
#     [
#         Input("crime-category-dropdown", "value"),
#         Input("time-slider", "value"),
#         Input("time-filter-dropdown", "value"),
#         Input("geo-level-dropdown", "value"),
#     ],
# )
# def update_map(**kwargs):
#     return map_crime_rate.create_choropleth(**kwargs)


# @app.callback(
#     [
#         Output("time-slider", "max"),
#         Output("time-slider", "marks"),
#         Output("time-slider", "value"),
#         Output("interval-component", "disabled"),
#     ],
#     [
#         Input("time-filter-dropdown", "value"),
#         Input("geo-level-dropdown", "value"),
#         Input("play-button", "n_clicks"),
#         Input("pause-button", "n_clicks"),
#         Input("interval-component", "n_intervals"),
#     ],
#     [State("interval-component", "disabled"), State("time-slider", "value")],
# )
# def update_time_slider_and_control_animation_callback(**kwargs):
#     return map_crime_rate.update_time_slider_and_control_animation(**kwargs)


# # ------ Beat crime type callbacks ------


# # Callback to update the plot based on the selected year
# @app.callback(Output("cluster-plot", "figure"), [Input("year-slider", "value")])
# def update_beat_crime_type(selected_year):
#     return beat_crime_type.update_figure(selected_year)
