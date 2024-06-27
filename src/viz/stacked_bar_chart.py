"stacked_bar_chart.py"

import pandas as pd
import plotly.graph_objects as go

from paths import DATA_STACKEDBC_FOLDER
from dash import dcc, html
from dash.dependencies import Input, Output

## LE TEMPLATE DE FICHIER A UTILISER POUR LES VISUALISATIONS
## Chaque fichier de visualisation doit contenir la fonction get_figure(data) qui retourne un objet figure de plotly
## Le nom du fichier est : "nom_de_la_visualisation.py"


# Import data
beat_count = pd.read_csv(DATA_STACKEDBC_FOLDER + "/beat_count.csv")
district_count = pd.read_csv(DATA_STACKEDBC_FOLDER + "/district_count.csv")
type_count = pd.read_csv(DATA_STACKEDBC_FOLDER + "/type_count.csv")


# J'ai aussi besoin d'une façon de choisir entre les 3 data sets (beat/district/type) 

#find a way to split data set in 2

district_true = district_count[district_count['Arrest']].sort_values(by='arrest_rate_district', ascending=False)
district_false = district_count[district_count['Arrest'] == False].sort_values(by='arrest_rate_district', ascending=False)

beat_true = beat_count[beat_count['Arrest']].sort_values(by='arrest_rate_beat', ascending=False)
beat_false = beat_count[beat_count['Arrest'] == False].sort_values(by='arrest_rate_beat', ascending=False)

type_true = type_count[type_count['Arrest']].sort_values(by='arrest_rate_type', ascending=False)
type_false = type_count[type_count['Arrest'] == False].sort_values(by='arrest_rate_type', ascending=False)

all_data = {"district": {"x" : [district_false["arrest_rate_district"], district_true["arrest_rate_district"]], "y" : [district_false['District'].apply(lambda x : str(int(x))), district_true['District'].apply(lambda x : str(int(x)))]},
        "beat": {"x" : [beat_false["arrest_rate_beat"], beat_true["arrest_rate_beat"]], "y" : [beat_false['Beat'].apply(lambda x : str(x)), beat_true['Beat'].apply(lambda x : str(x))]},
        "type": {"x" : [type_false["arrest_rate_type"], type_true["arrest_rate_type"]], "y" : [type_false['Primary.Type'], type_true['Primary.Type']]}}


# transform district into string
#y = str(district_false['District'])


#creation viz

def create_stacked_bar(mode="district"):
    # Create the figure
    fig = go.Figure()

    # Add traces
    fig.add_trace(
        go.Bar(
            x = all_data[mode]['x'][0],
            y = all_data[mode]['y'][0],
            name=f"{mode.capitalize()} Not Arrested",
            orientation = 'h',
            hovertemplate=get_hover_template(mode, "Not Arrested"),
            )
        )
    fig.add_trace(
        go.Bar( 
            x = all_data[mode]['x'][1],
            y = all_data[mode]['y'][1],
            name = f"{mode.capitalize()} Arrested",
            orientation = 'h',
            hovertemplate=get_hover_template(mode, "Arrested")
        )
    )

    # Set layout
    fig.update_layout(
        title=f"Arrest rate for each {mode.capitalize()}",
        barmode="stack",
        title_x=0.5,
        xaxis=dict(fixedrange=True),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    if mode == "district":
        fig.update_layout(
            xaxis=dict(title="Arrest rate"),
            yaxis=dict(title="District"),
        )
    elif mode == "beat":
        fig.update_layout(
            xaxis=dict(title="Arrest rate"),
            yaxis=dict(title="Beat"),
        )
    elif mode == "type":
        fig.update_layout(
            xaxis=dict(title="Arrest rate"),
            yaxis=dict(title="Type"),
        )

    return fig


def get_figure(_data):
    fig = create_stacked_bar()
    return fig

# hover template

def get_hover_template(mode, is_arrested):
    hovertext = ""
    if mode == "district":
        hovertext += "<b>District %{y}</b><br>Rate of " + is_arrested + ": %{x} %"
    elif mode == "beat":
        hovertext += "<b>Beat %{y}</b><br>Rate of " + is_arrested + ": %{x} %"
    elif mode == "type":
        hovertext += "<b>%{y}</b><br>Rate of " + is_arrested + ": %{x} %"
    return hovertext + "<extra></extra>"

def get_html(figure):
    return html.Div(
        className="histogram-container",
        children=[
            dcc.Graph(
                className="histogram",
                id="stacked_bar_chart",
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
                            html.H4("Category:"),
                            dcc.Dropdown(
                                id="stacked-bar-chart-dropdown",
                                options=[
                                    {"label": "District", "value": "district"},
                                    {"label": "Beats", "value": "beat"},
                                    {"label": "Type", "value": "type"},
                                ],
                                value="district",
                                clearable=False,
                                style={"width": "100%", "color": "black"},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

def get_callbacks(app):
    
    @app.callback(
        Output("stacked_bar_chart", "figure"),
        [
            Input("stacked-bar-chart-dropdown", "value"),
            Input("stacked_bar_chart", "figure"),
        ],
    )
    def stacked_bar_chart_callback(value, figure):
        return create_stacked_bar(value)
