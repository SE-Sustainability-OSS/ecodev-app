"""
Module implementing an example of customisable footer components.
"""
import dash_mantine_components as dmc
from dash import dcc
from ecodev_front import app_logo

from app.constants import COMM_CHANNEL_URL
from app.constants import FEEDBACK_URL


def main_footer() -> dmc.Group:
    """
    Render's the app's main footer
    """
    return dmc.Group([
        dcc.Markdown(
            f'##### Questions? Bugs? [Contact us here]({COMM_CHANNEL_URL})',
            link_target='_blank',
        ),
        dcc.Markdown(
            f'##### Any [comments or feedback]({FEEDBACK_URL}) is welcome!',
            link_target='_blank',
        ),
        dmc.Affix(app_logo(), position={'bottom': 12, 'right': 20}),
    ], justify='center', align='center')
