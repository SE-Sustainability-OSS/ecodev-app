"""
Module creating an example datatable.

NB: here the page structure is trivial. Would you need several components/plots, create subfolders
components and plots below the page folder.
"""
import dash_ag_grid as dag
from ecodev_front.components import data_table
from plotly.data import iris

from app.pages.data_table_page import DATA_TABLE


def get_example_table() -> dag.AgGrid:
    """
    Example datatable
    """
    default_col_def = {
        'resizable': True,
        'sortable': True,
        'wrapHeaderText': True,
        'autoHeaderHeight': True,
        'wrapText': True,
        'autoHeight': True,
    }

    row_style = {
        'styleConditions': [
            {
                'condition': "params.data.species === 'setosa'",
                'style': {'backgroundColor': '#D585C7'},
            },
            {
                'condition': "params.data.species === 'versicolor'",
                'style': {'backgroundColor': '#60AFFF'},
            },
            {
                'condition': "params.data.species === 'virginica'",
                'style': {'backgroundColor': '#ADFFE2'},
            },
        ]
    }

    dash_grid_options = {
        'colResizeDefault': 'shift',
        'suppressRowHoverHighlight': True,
        'rowSelection': 'single',
        'headerHeight': 30,
        'groupHeaderHeight': 30,
    }
    return data_table(
        id=DATA_TABLE,
        df=iris(),
        default_col_def=default_col_def,
        row_style=row_style,
        dash_grid_options=dash_grid_options,
        style={'height': '80vh'},
    )
