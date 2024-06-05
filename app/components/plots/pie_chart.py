"""
Module implementing an example of a  pie chart with Plotly
"""
from dash import dcc
from plotly import express as px


def pie_chart() -> dcc.Graph:
    """
    Example of a pie chart with Plotly.
    Note: Only thing of note is the return of a dcc.Graph component with 'graph' className.
    """
    df = px.data.gapminder().query('year == 2007').query("continent == 'Europe'")
    fig = px.pie(df, values='pop', names='country', hole=0.3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(margin={'t': 10, 'l': 10, 'b': 10, 'r': 10}, showlegend=False)
    return dcc.Graph(figure=fig, className='graph')
