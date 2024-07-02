"""
Module implementing an example of customisable footer components.
"""
import dash_mantine_components as dmc
from dash import callback
from dash import dcc
from dash import html
from dash import Input
from dash import Output
from dash import State
from ecodev_core import get_access_token
from ecodev_core import is_authorized_user

from app.constants import COMM_CHANNEL_URL
from app.constants import FEEDBACK_URL
from app.constants import FOOTER
from app.constants import TOKEN


def app_footer() -> html.Div:
    """
    Example of implementation of an app's footer.
    """
    return _footer(
        dmc.Group(
            [
                dcc.Markdown(
                    f'##### Questions? Bugs? [Contact us here]({COMM_CHANNEL_URL})',
                    link_target='_blank',
                ),
                dcc.Markdown(
                    f'##### Any [comments or feedback]({FEEDBACK_URL}) is welcome!',
                    link_target='_blank',
                ),
            ]
        )
    )


def _footer(
    children: dmc.Group,
    color: str = '#0066A1',
    display: str = 'flex',
) -> html.Div:
    """
    Main app footer
    """
    return html.Div(
        children,
        style={
            'paddingBottom': '10px',
            'backgroundColor': color,
            'color': 'white',
            'display': display,
            'textAlign': 'center',
            'alignContent': 'center',
            'justifyContent': 'center',
        },
    )


# @callback(
#     Output(FOOTER, 'children'),
#     Input(TOKEN, 'data'),
# )
# def show_hide_footer(token) -> dmc.Group:
#     """
#     Navbar update. If no valid token is present in the store, return the login component.
#     Otherwise, return the full navbar with all the page app.
#     """
#     return app_footer() if is_authorized_user(get_access_token(token)) else None

