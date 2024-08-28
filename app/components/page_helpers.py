"""
Module implementing a generic page wrapper to handle authentication
"""
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import no_update
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from ecodev_core import attempt_to_log
from ecodev_core import engine
from ecodev_core import get_access_token
from ecodev_core import get_user
from ecodev_core import Permission
from ecodev_core import safe_get_user
from ecodev_front import FOOTER_ID
from ecodev_front import HEADER_ID
from ecodev_front import LOGIN_BTN_ID
from ecodev_front import LOGIN_PASSWORD_INPUT_ID
from ecodev_front import LOGIN_USERNAME_INPUT_ID
from ecodev_front import LOGOUT_BTN_ID
from ecodev_front import TOKEN
from ecodev_front import URL
from fastapi import HTTPException
from sqlmodel import Session

from app.components.footer import app_footer
from app.components.navbar import navbar
from app.components.navbar import navbar_login_header

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


@callback(Output(HEADER_ID, 'children'),
          Output(FOOTER_ID, 'children'),
          Input(TOKEN, 'data'),
          Input(URL, 'pathname'))
def update_navbar_footer_on_login(token: dict[str, str | None], pathname):
    """
    Navbar update. If no valid token is present in the store, return only navbar header.
    Otherwise, return the full navbar with all the page app.
    """
    if user := safe_get_user(token):
        return navbar(user.permission == Permission.ADMIN), app_footer()
    return navbar_login_header(), None


@callback(
    Output(TOKEN, 'data', allow_duplicate=True),
    Input(LOGIN_BTN_ID, 'n_clicks'),
    State(LOGIN_USERNAME_INPUT_ID, 'value'),
    State(LOGIN_PASSWORD_INPUT_ID, 'value'),
    prevent_initial_call=True,
)
def user_login(n_clicks: int, username: str, password: str):
    """
    Callback when user presses the login button.

    NB: using an attempt_to_log variation from ecodev_core to avoid
    raising an error on server-side, but rather on client-side.
    """
    if not n_clicks:
        raise no_update
    try:
        with Session(engine) as session:
            token = attempt_to_log(username, password, session)
        return {TOKEN: token}
    except HTTPException:
        return {TOKEN: {}}


@callback(
    Output(TOKEN, 'data', allow_duplicate=True),
    Output(URL, 'pathname', allow_duplicate=True),
    Input(LOGOUT_BTN_ID, 'n_clicks'),
    prevent_initial_call=True,
)
def user_logout(n_clicks: int):
    """
    Reset token value when user logs out.
    """
    if not n_clicks:
        raise PreventUpdate
    return {TOKEN: None}, '/'
