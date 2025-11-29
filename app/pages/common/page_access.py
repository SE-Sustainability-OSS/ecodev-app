"""
File containing function to check if the user has access to a page.
"""
import dash_mantine_components as dmc
from dash import html
from ecodev_core import Permission
from ecodev_core import safe_get_user


NOT_AUTHORIZED = dmc.Center(dmc.Alert(title='Unauthorized',
                                      children='You don\'t have access to this page.',
                                      color='red',
                                      w='90vw'))


def check_page_access(token: dict,
                      page: dmc.Stack | list | dmc.Card | dmc.Text | dmc.Container | html.Div,
                      admin: bool = False
                      ) -> dmc.Center | list:
    """
    Returns a NOT_AUTHORIZED if the token is not filled or if the user is not authorized to connect.
    If admin is True, the user is only authorized to see passed page if he has admin privileges.
    """
    if not (user := safe_get_user(token)):
        return NOT_AUTHORIZED

    return page if (not admin or user.permission == Permission.ADMIN) else NOT_AUTHORIZED
