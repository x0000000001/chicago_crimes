"""
LE TEMPLATE DE FICHIER A UTILISER POUR LES VISUALISATIONS
Chaque fichier de visualisation doit contenir la fonction get_figure(data) qui retourne un objet figure de plotly
Le nom du fichier est : "nom_de_la_visualisation.py"
"""

import plotly.graph_objects as go


def get_figure(_data):
    """
    Returns a plotly figure object

    Args:
        data: The data to display
    Returns:
        The figure to be displayed.
    """
    fig = go.Figure()
    return fig


def get_hover_template():
    """
    Returns the hover template for the figure.

    Returns:
        The hover template.
    """
    return "No data to show"
