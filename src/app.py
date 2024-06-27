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
                                                "A temporal analysis",
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-text-content",
                                            children=[
                                                html.P(
                                                    "Crimes do not all happen at the same intensities, \
                                                    at the same time. Play with this barchart to see which \
                                                    crimes happen when. See, for instance, how thefts \
                                                    happen mostly during the afternoon, or kidnappings \
                                                    have a peak on fridays."
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
                                    className="overlay hidden",
                                ),
                                html.Section(
                                    className="modal hidden",
                                    children=[
                                        html.Div(
                                            className="modal-content",
                                            children=[
                                                html.H2("About the categorization"),
                                                html.P(
                                                    "Here is how we grouped the crime types:"
                                                ),
                                                html.Ul(
                                                    children=[
                                                        html.Li(
                                                            children = [
                                                                html.Strong("Violent Crimes:"),
                                                                " Battery, Robbery, Assault, Stalking, Criminal Sexual Assault, Homicide, Kidnapping, Sex Offense, Intimidation, and Domestic Violence."
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children = [
                                                                html.Strong("Crimes Against Children:"),
                                                                " Offenses Involving Children."
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children = [
                                                                html.Strong("Property Crimes:"),
                                                                " Theft, Criminal Damage, Burglary, Motor Vehicle Theft, Criminal Trespass, and Arson."
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children = [
                                                                html.Strong("Public Order Crimes:"),
                                                                " Weapons Violation, Prostitution, Public Peace Violation, Concealed Carry License Violation, Liquor Law Violation, Obscenity, Gambling, and Public Indecency."
                                                            ]
                                                        ),

                                                        html.Li(
                                                            children = [
                                                                html.Strong("White Collar Crimes:"),
                                                                " Deceptive Practice."
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children = [
                                                                html.Strong("Drug Offenses:"),
                                                                " Narcotics and Other Narcotic Violations."
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children = [
                                                                html.Strong("Miscellaneous Crimes:"),
                                                                " Other Offenses, Interference with Public Officer, Non-Criminal, Human Trafficking, Ritualism, and various other non-criminal classifications."
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            className="modal-flex",
                                            children=[
                                                html.Button(
                                                    className="btn btn-close",
                                                    children="Close",
                                                )
                                            ]
                                        ),
                                    ],
                                ),
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
                                            className="viz-text-content map-viz-text-content",
                                            children=[
                                                html.P("This chloropleth map shows the distribution of crimes in Chicago. The color intensity denounces the number of crime reported according to the search parameters configurations."),
                                                html.P("In order to allow for a more effective comparison of crime rates within the same category across districts and beats, rather than analyzing each type individually, we regrouped the crimes by using general categories."),
                                                html.P("This re categorization is designed to provide you with actionable insights, making it easier to identify trends and make informed decisions."),
                                                html.P("It will also enable a more effective and strategic planning, helping you allocate resources more efficiently and take more targeted actions to improve public safety."),
                                                
                                            ]
                                        ),
                                        html.Button(
                                            className="btn btn-open",
                                            children="More information",
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
                                                "Districts, beats and arrest rates",
                                            ],
                                        ),
                                        html.Div(
                                            className="viz-text-content",
                                            children=[
                                                html.P(
                                                    "Should someone be arrested for theft ? assault ? drug offenses ? \
                                                    While this obviously depends on the type of crime, it seems \
                                                    to be correlated with the geographical location of the crime too..."
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
