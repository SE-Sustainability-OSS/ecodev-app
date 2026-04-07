"""
Module implementing the app's header components.
"""
import dash_mantine_components as dmc
from dash import html
from ecodev_core import logger_get
from ecodev_front import app_header_name
from ecodev_front import app_logo

from app.constants import APP_NAME

log = logger_get(__name__)


def display_app_header() -> html.Div:
    """
    Renders the app header display.
    """
    return dmc.Box([
        dmc.Box(
            app_logo(ratio=300/91, width='100px'),
            visibleFrom='md',
            style={'position': 'absolute', 'left': 10, 'top': 0}
        ),
        dmc.Center(
            app_header_name(APP_NAME),
            w='100%'
        ),
    ], w='100%', mt=5, style={'position': 'relative'})
