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
            children=[
                dcc.Graph(figure=figures[figure_file]) for figure_file in figures
            ],
        ),
    ],
)
