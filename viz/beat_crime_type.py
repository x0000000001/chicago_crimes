import plotly.graph_objects as go

## LE TEMPLATE DE FICHIER A UTILISER POUR LES VISUALISATIONS
## Chaque fichier de visualisation doit contenir la fonction get_figure(data) qui retourne un objet figure de plotly
## Le nom du fichier est : "nom_de_la_visualisation.py"

import pandas as pd
import plotly.express as px
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

# Load the data
file_path = 'Crimes_-_2001_to_Present_20240611.csv'
df = pd.read_csv(file_path)

# Convert 'Date' to datetime and extract the year
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# Initialize the Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1)},
        step=None
    ),
    dcc.Graph(id='cluster-plot')
])

# Callback to update the plot based on the selected year
@app.callback(
    Output('cluster-plot', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_year):
    # Filter data for the selected year
    df_year = df[df['Year'] == selected_year]

    # Group by 'Beat' and 'Primary Type' to get arrest counts
    grouped = df_year.groupby(['Beat', 'Primary Type']).size().reset_index(name='Arrest Count')

    # Pivot table to create a matrix for clustering
    pivot_df = grouped.pivot(index='Beat', columns='Primary Type', values='Arrest Count').fillna(0)

    # Perform t-SNE for dimensionality reduction
    tsne = TSNE(n_components=2, random_state=0)
    tsne_result = tsne.fit_transform(pivot_df)

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=5, random_state=0)
    pivot_df['cluster'] = kmeans.fit_predict(pivot_df)

    # Create a DataFrame with t-SNE results and cluster labels
    tsne_df = pd.DataFrame(tsne_result, columns=['TSNE Component 1', 'TSNE Component 2'])
    tsne_df['cluster'] = pivot_df['cluster'].values
    tsne_df['Beat'] = pivot_df.index

    # Create the plot
    fig = px.scatter(tsne_df, x='TSNE Component 1', y='TSNE Component 2', color='cluster', hover_data=['Beat'])
    fig.update_layout(title=f'Cluster Analysis for Year {selected_year}', xaxis_title='t-SNE Component 1', yaxis_title='t-SNE Component 2')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    
def get_figure(data):
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