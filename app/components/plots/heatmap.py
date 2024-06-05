"""
Module implementing an example of a heat map with Plotly
"""
from dash import html
from ecodev_front import graph_box
from plotly import express as px


def heat_map() -> html.Div:
    """
    Example of a heat map with Plotly.
    Note: Only thing of note is the return of a dcc.Graph component with 'graph' className.
    """
    data = [[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
    fig = px.imshow(
        data,
        labels=dict(x='Day of Week', y='Time of Day', color='Productivity'),
        x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        y=['Morning', 'Afternoon', 'Evening'],
    )
    fig.update_xaxes(side='top')
    fig.update_layout(showlegend=False)
    return graph_box(fig)
