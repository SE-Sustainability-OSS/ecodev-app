"""
Module implementing a generic page wrapper to handle authentication
"""
import dash_mantine_components as dmc
from dash import html
from ecodev_core import get_access_token
from ecodev_core import get_user
from ecodev_core import Permission


NOT_AUTHORIZED = [html.P('Unauthorized. Please login to access')]


def generic_page(token: dict,
                 page: dmc.Stack | list | dmc.Card | dmc.Text | dmc.Container | html.Div,
                 admin: bool = False
                 ) -> dmc.Stack | list:
    """
    Returns a NOT_AUTHORIZED if the token is not filled or if the user is not authorized to connect.
    If admin is True, the client is only authorized to see passed page if he has admin privileges.
    """
    if not (user := get_user(get_access_token(token))):
        return NOT_AUTHORIZED

    return page if (not admin or user.permission == Permission.ADMIN) else NOT_AUTHORIZED
