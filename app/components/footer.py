"""
Module implementing an example of customisable footer components.
"""
import dash_mantine_components as dmc
from dash import dcc

from app.constants import COMM_CHANNEL_URL
from app.constants import FEEDBACK_URL


def app_footer() -> dmc.Group:
    """
    Example of implementation of an app's footer.
    """
    return dmc.Group([
        dcc.Markdown(
            f'##### Questions? Bugs? [Contact us here]({COMM_CHANNEL_URL})',
            link_target='_blank',
        ),
        dcc.Markdown(
            f'##### Any [comments or feedback]({FEEDBACK_URL}) is welcome!',
            link_target='_blank',
        )
    ], justify='center')
