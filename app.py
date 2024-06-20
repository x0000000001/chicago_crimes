# -*- coding: utf-8 -*-
"""
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file contains the source code for project.
"""

import importlib

import dash
import pandas as pd
from dash import html

# from viz import map_crime_rate, beat_crime_type

# TODO make functions in paths for files
# TODO unify categories of crimes, maybe choose

app = dash.Dash(__name__)
app.title = "Chicago Crimes | INF8808"

# TODO test delays with real dataset
# DATA_PATH = "assets/data/crimes.csv" # full dataset
DATA_PATH = "assets/data/crimes_reduced.csv"  # 1000 times reduced dataset

with open(DATA_PATH, encoding="utf-8") as data_file:
    data = pd.read_csv(data_file)

# Load figures
figures_files = ["multiline", "histogram", "map", "cluster"]

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
