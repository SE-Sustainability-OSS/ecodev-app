"""
Module implementing an example of a bar chart with Plotly
"""
from dash import dcc
from plotly import express as px


def bar_chart() -> dcc.Graph:
    """
    Example of a bar chart with Plotly.
    Note: Only thing of note is the return of a dcc.Graph component with 'graph' className.
    """
    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x='year', y='pop')
    fig.update_layout(margin={'t': 10, 'l': 10, 'b': 10, 'r': 10})

    return dcc.Graph(figure=fig, className='graph')
