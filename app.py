# -*- coding: utf-8 -*-

"""
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file contains the source code for TP4.
"""

import dash
import dash_html_components as html

import pandas as pd

app = dash.Dash(__name__)
app.title = "TP4 | INF8808"

DATA_PATH = "../src/assets/data/crimes.csv"

with open(DATA_PATH, encoding="utf-8") as data_file:
    data = pd.read_csv(data_file)

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
                # our graphs
            ],
        ),
    ],
)
