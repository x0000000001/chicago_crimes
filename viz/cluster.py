"""
Crime rate per crime type and beat visualization.
"""

import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

import paths
from app import app

# FIXME slider ugly


def get_html(figure):
    # read min and max years
    with open(f"{paths.DATA_CLUSTER_FOLDER}/min_max_years", "r", encoding="utf-8") as f:
        min_year = int(f.readline())
        max_year = int(f.readline())

    return html.Div(
        className="cluster-plot-container",
        children=[
            dcc.Graph(
                className="cluster-plot",
                id="cluster-plot",
                figure=figure,
                config={"displayModeBar": False},
            ),
            html.Div(
                className="cluster-plot-params",
                children=[
                    html.H2("Parameters"),
                    html.Div(
                        [
                            dcc.Slider(
                                id="year-slider",
                                min=min_year,
                                max=max_year,
                                value=min_year,
                                marks={
                                    str(year): str(year)
                                    for year in range(min_year, max_year + 1)
                                },
                                step=None,
                            ),
                        ],
                        style={"width": "100%", "padding": "0px 20px 20px 20px"},
                    ),
                ],
            ),
        ],
    )


def create_figure(selected_year):
    tsne_df = pd.read_csv(f"{paths.DATA_CLUSTER_FOLDER}/cluster_{selected_year}.csv")

    # Create the plot
    fig = px.scatter(
        tsne_df,
        x="TSNE Component 1",
        y="TSNE Component 2",
        color="cluster",
        hover_data=["Beat"],
    )

    fig.update_layout(
        title=dict(text=f"Cluster Analysis for Year {selected_year}", font=dict(color="white")),
        xaxis_title=dict(text="t-SNE Component 1", font=dict(color="white")),
        yaxis_title=dict(text="t-SNE Component 2", font=dict(color="white")),
        xaxis=dict(fixedrange=True, tickfont=dict(color="white")),
        yaxis=dict(fixedrange=True, tickfont=dict(color="white")),
        title_x=0.5,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )

    return fig


def get_figure(data):
    """
    Returns a plotly figure object

    Args:
        data: The data to display
    Returns:
        The figure to be displayed.
    """
    return create_figure(data["Year"].min())


def get_hover_template():
    """
    Returns the hover template for the figure.

    Returns:
        The hover template.
    """
    return "Beat: %{hover_data[0]}"


# Callback to update the plot based on the selected year
@app.callback(Output("cluster-plot", "figure"), [Input("year-slider", "value")])
def update_figure_callback(selected_year):
    return create_figure(selected_year)
