"stacked_bar_chart.py"

import pandas as pd
import plotly.graph_objects as go

from paths import DATA_STACKEDBC_FOLDER

## LE TEMPLATE DE FICHIER A UTILISER POUR LES VISUALISATIONS
## Chaque fichier de visualisation doit contenir la fonction get_figure(data) qui retourne un objet figure de plotly
## Le nom du fichier est : "nom_de_la_visualisation.py"


# Import data
beat_count = pd.read_csv(DATA_STACKEDBC_FOLDER + "/beat_count.csv")
district_count = pd.read_csv(DATA_STACKEDBC_FOLDER + "/district_count.csv")
type_count = pd.read_csv(DATA_STACKEDBC_FOLDER + "/type_count.csv")

# Calculate arrest rate
# J'ai besoin d'une façon de calculer un pourcentage pour true + false pour chaque beat/district/type
# J'ai aussi besoin d'une façon de choisir entre les 3 data sets (beat/district/type)

# creation viz


def create_stacked_bar(x, y):
    # Create the figure
    fig = go.Figure()

    # Add traces
    fig.add_trace(
        data=[
            go.Bar(
                "x= ",
                "y= ",
                name="Not Arrested",
                visible=True,
                color="#f01405",
                orientation="h",
            ),
            go.Bar(
                "x = ",
                "y = ",
                name="Arrested",
                visibility=True,
                color="#071cfa",
                orientation="h",
            ),
        ]
    )

    # Set layout
    fig.update_layout(
        title="Arrest rate for each Beat/District/Type",
        xaxis_title="",
        yaxis_title="",
        barmode="stack",
        title_x=0.5,
    )

    return fig


def get_figure(_data):
    fig = create_stacked_bar("x", "y")
    return fig


# hover template
# multiply y * 100 to get percentage


def get_hover_template():
    return "Rate: %{y}"
