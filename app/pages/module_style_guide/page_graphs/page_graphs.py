"""
Module implementing the buttons components page of the style-guide
"""
import dash_mantine_components as dmc
import plotly.express as px
from dash import Input
from dash import Output
from dash import State
from ecodev_core import logger_get
from ecodev_front import CHILDREN
from ecodev_front import DATA
from ecodev_front import graph_box
from ecodev_front import header_layout
from ecodev_front import Page
from ecodev_front import TOKEN

from app.constants import PROJECT_ID_STORE
from app.pages.common.custom_callback import safe_callback


log = logger_get(__name__)

PAGE_GRAPHS = Page(
    module=__name__,
    name='graphs',
    icon='codicon:graph',
    title='Graphs',
    description='Example of graphs using our custom plotly colors & theme.',
    layout=header_layout
)


@safe_callback(Output(PAGE_GRAPHS.id, CHILDREN),
               Input(TOKEN, DATA),
               State(PROJECT_ID_STORE, DATA))
def render_page(token: dict, project_id: int):
    """
    Renders page's initial layout / content.
    NOTE: Page access is checked via the safe_callback decorator,
    to disable this check, set check_access to False.
    """
    return dmc.Stack([
        bar_chart_example(),
        scatter_plot_example(),
        heatmap_example(),
        histogram_example()
    ], align='flext-start', gap='30px', w='95%', m='auto')


def bar_chart_example() -> dmc.Stack:
    """
    Renders a bar chart
    """
    df = px.data.medals_long()
    fig = px.bar(df, x='medal', y='count',
                 color='nation',
                 text_auto=True,
                 title='Example bar chart with plotly template')
    return graph_box(fig)


def scatter_plot_example() -> dmc.Stack:
    """
    Renders scatter plot
    """
    df = px.data.iris()
    fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species',
                     size='petal_length',
                     hover_data=['petal_width'],
                     title='Example scatter plot with plotly template')
    return graph_box(fig)


def heatmap_example() -> dmc.Stack:
    """
    Renders a heatmap graph
    """
    df = px.data.tips()
    fig = px.density_heatmap(df, x='total_bill', y='tip',
                             title='Example heatmap with plotly template')
    return graph_box(fig)


def histogram_example() -> dmc.Stack:
    """
    Renders a histogram
    """
    df = px.data.tips()
    fig = px.histogram(df, x='total_bill', y='tip', color='day', marginal='rug',
                       hover_data=df.columns,
                       title='Example histogram with plotly template')
    return graph_box(fig)
