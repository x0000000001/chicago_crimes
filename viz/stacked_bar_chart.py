import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd


colors = ["#4287f5", "#e02222"]

df = pd.read_csv("beat_count.csv")


df["Beat"] = df.Beat.astype(str)

df["norm_beat"] = df["count"] / df.groupby("Beat")["count"].transform("sum")


x_data = df["norm_beat"]
y_data = df["Beat"]


def get_figure(data):
    """
    Returns a plotly figure object

    Args:
        data: The data to display
    Returns:
        The figure to be displayed.
    """
    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(
                go.Bar(
                    x=[xd[i]],
                    y=[yd],
                    orientation="h",
                    marker=dict(
                        color=colors[i], line=dict(color="rgb(248, 248, 249)", width=1)
                    ),
                )
            )

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=True,
            showticklabels=True,
            zeroline=True,
        ),
        yaxis=dict(
            showgrid=False,
            showline=True,
            showticklabels=True,
            zeroline=True,
        ),
        barmode="stack",
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        margin=dict(l=120, r=10, t=140, b=80),
        showlegend=True,
    )
    annotations = []
    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(
            dict(
                xref="paper",
                yref="y",
                x=0.14,
                y=yd,
                xanchor="right",
                text=str(yd),
                font=dict(family="Arial", size=14, color="rgb(67, 67, 67)"),
                showarrow=False,
                align="right",
            )
        )
        # labeling the first percentage of each bar (x_axis)
        annotations.append(
            dict(
                xref="x",
                yref="y",
                x=xd[0] / 2,
                y=yd,
                text=str(xd[0]) + "%",
                font=dict(family="Arial", size=14, color="rgb(248, 248, 255)"),
                showarrow=False,
            )
        )

        space = xd[0]
        for i in range(1, len(xd)):
            # labeling the rest of percentages for each bar (x_axis)
            annotations.append(
                dict(
                    xref="x",
                    yref="y",
                    x=space + (xd[i] / 2),
                    y=yd,
                    text=str(xd[i]) + "%",
                    font=dict(family="Arial", size=14, color="rgb(248, 248, 255)"),
                    showarrow=False,
                )
            )
            space += xd[i]

    fig.update_layout(annotations=annotations)

    return fig


def get_hover_template():
    """
    Returns the hover template for the figure.

    Returns:
        The hover template.
    """
    hover_template = (
        '<span style="font-family: Arial; font-size: 24px; font-color: Black">%{y_data}</span><br></br>'
        + "<br><b></b>%{x_data}%%"
        "of lines</br><extra></extra>"
    )
    return "No data to show"
