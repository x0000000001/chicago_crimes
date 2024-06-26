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

from paths import DATA_REDUCED_PATH

# from viz import map_crime_rate, beat_crime_type

# TODO make functions in paths for files
# TODO unify categories of crimes, maybe choose

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Chicago Crimes | INF8808"

server = app.server

with open(DATA_REDUCED_PATH, encoding="utf-8") as data_file:
    data = pd.read_csv(data_file)

# Load figures
figures_files = ["multiline", "histogram", "map", "cluster", "stacked_bar_chart"]

figures = {}
html_elements = {}

for figure_file in figures_files:
    module = importlib.import_module(f"viz.{figure_file}")
    figures[figure_file] = figure = module.get_figure(data)
    html_elements[figure_file] = module.get_html(figure)
    module.get_callbacks(app)

app.layout = html.Div(
    className="content",
    children=[
        html.Div(className="progress"),
        html.Header(children=[]),
        html.Main(
            children=[
                html.A(
                    href="#",
                    className="up-button",
                    children=html.Img(
                        className="up-button-img",
                        src="assets/img/up_button.png",
                    ),
                ),
                html.Div(
                    className="title-page-container",
                    children=[
                        html.Div(
                            className="background-color-left",
                        ),
                        html.Img(
                            src="assets/img/chicago4k.jpg",
                            className="background-image",
                        ),
                        html.H1(
                            "Spatial and temporal analyses of Chicago criminals trends since 2001"
                        ),
                        html.H2("How did crimes evolved since 2001 in Chicago ?"),
                        html.P(
                            "Summer 2024 - INF8808E - Data Visualization - Hellen Dos Santos Vasques"
                        ),
                        html.P(
                            "A project by Lucas Bertinchamp, Leila Rouga, Hélène Genet, Antoine Toussaint, Jeremy Tsatas, Md. Radwan Rahman"
                        ),
                        html.A(
                            href="#beginning",
                            children=html.Img(
                                src="assets/img/up_button.png",
                                className="button-start",
                            ),
                        ),
                    ],
                ),
                html.Div(
                    className="section-slider",
                    id="beginning",
                    children=[
                        html.Div(
                            className="section-slider-sticky",
                            children=[
                                html.Div(
                                    className="slider-elements",
                                    children=[
                                        html.Div(
                                            className="chicago-intro",
                                            children=[
                                                html.H2("The city of Chicago"),
                                                html.P(
                                                    "Chicago, located on the shores of Lake Michigan, is the third-largest city in the United States, renowned for its iconic architecture, vibrant cultural scene, and historic sports teams."
                                                ),
                                                html.Br(),
                                                html.P(
                                                    "However, the city faces ongoing challenges with crime, impacting the daily lives of its residents."
                                                ),
                                            ],
                                        ),
                                        html.Img(
                                            src="assets/img/chicago1.jpg",
                                            alt="Chicago skyline",
                                        ),
                                        html.Img(
                                            src="assets/img/chicago2.jpg",
                                            alt="Chicago skyline",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Ul(
                    id="all-viz",
                    children=[
                        html.Li(
                            className="section-viz",
                            id="viz_1",
                            children=[
                                html.Div(
                                    className="viz-content",
                                    children=[
                                        html.Div(
                                            className="viz-text-title",
                                            children=[
                                                "What about crimes in Chicago ?",
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-text-content",
                                            children=[
                                                html.P(
                                                    "Chicago is a city with a high crime rate. Let's see with a general visualisation how the number of crimes has evolved since 2001 for several types of crimes. Here are shown the types of crimes that are representative of 95% of crimes in Chicago."
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-container",
                                            children=html_elements["multiline"],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Li(
                            className="section-viz black-background",
                            id="viz_2",
                            children=[
                                html.Div(
                                    className="viz-content",
                                    children=[
                                        html.Div(
                                            className="viz-text-title",
                                            children=[
                                                "What about crimes in Chicago ?",
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-text-content",
                                            children=[
                                                html.P(
                                                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-container",
                                            children=html_elements["histogram"],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Li(
                            className="map-section-viz",
                            id="viz_3",
                            children=[
                                html.Div(
                                    className="viz-content",
                                    id="map-text",
                                    children=[
                                        html.Div(
                                            className="viz-text-title",
                                            children=[
                                                "A spatial analysis",
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-text-content",
                                            children=[
                                                html.P("This chloropleth map shows the distribution of crimes in Chicago. The color intensity denounces the number of crime reported according to the search parameters configurations."),
                                                html.Br(),
                                                html.P("The following visualization addresses these spatial analysis points:"),
                                                html.P("• The regions where crimes are more frequent. | • Patterns or trends linking districts to specific criminal activities."),
                                                html.P("• Do certain police beats handle more crimes than others? | • Types of crimes are most commonly associated with specific beats"),
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-container",
                                            children=html_elements["map"],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Li(
                            className="section-viz black-background",
                            id="viz_4",
                            children=[
                                html.Div(
                                    className="viz-content",
                                    children=[
                                        html.Div(
                                            className="viz-text-title",
                                            children=[
                                                "Do some police beats arrest more people for specific types of crimes?",
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-text-content",
                                            children=[
                                                html.P(
                                                    "Analysis of the arrest patterns for different types of crimes across various police beats in Chicago."
                                                    ""
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-container",
                                            children=html_elements["cluster"],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Li(
                            className="section-viz final-viz",
                            id="viz_5",
                            children=[
                                html.Div(
                                    className="viz-content",
                                    children=[
                                        html.Div(
                                            className="viz-text-title",
                                            children=[
                                                "What about crimes in Chicago ?",
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-text-content",
                                            children=[
                                                html.P(
                                                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-container",
                                            children=html_elements["stacked_bar_chart"],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        ),
    ],
)

# Use start button to go to the next section
@app.callback(
    dash.dependencies.Output("button-start", "style"),
    dash.dependencies.Input("button-start", "n_clicks"),
)
def start_button(n_clicks):
    if n_clicks:
        return {"display": "none"}
    return {"display": "block"}


if __name__ == "__main__":
    app.run_server(debug=True)
