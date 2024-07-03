"""
Module creating the app_template tool dash app
"""
import dash
from dash import callback
from dash import Dash
from dash import Input
from dash import no_update
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from ecodev_core import attempt_to_log
from ecodev_core import create_db_and_tables
from ecodev_core import engine
from ecodev_core import logger_get
from ecodev_core import Permission
from ecodev_core import safe_get_user
from ecodev_core import upsert_app_users
from ecodev_front import dash_base_layout
from ecodev_front import FOOTER_ID
from ecodev_front import LOGIN_BTN_ID
from ecodev_front import LOGIN_PASSWORD_INPUT_ID
from ecodev_front import LOGIN_USERNAME_INPUT_ID
from ecodev_front import LOGOUT_BTN_ID
from ecodev_front import NAVBAR_ID
from ecodev_front import TOKEN
from ecodev_front import URL
from fastapi import HTTPException
from flask import Flask
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from sqlmodel import Session

import app.db_model as db_model
from app.components.footer import app_footer
from app.constants import ASSETS_DIR
from app.constants import DATA_DIR
from app.constants import DUMMY_OUTPUT
from app.pages import navbar
from app.pages import navbar_login_header

log = logger_get(__name__)


class DashAppSettings(BaseSettings):
    """
    Settings class to control the app behaviour.

    Attributes are:
        - debug: whether to use debug or not.
        - gunicorn_setup: should be false locally, true in production
    """

    debug: bool | None = True
    gunicorn_setup: bool = True
    model_config = SettingsConfigDict(env_file='.env')


DASH_APP_SETTINGS = DashAppSettings()
DEBUG = DASH_APP_SETTINGS.debug


def init_dash_app() -> Dash:
    """
    Initialize the dash application, running all what need to be run before startup.
    """
    log.info('Initializing dash app')
    create_db_and_tables(db_model.AppUser)
    if (file_path := DATA_DIR / 'users.json').exists():
        with Session(engine) as session:
            upsert_app_users(file_path, session)
    return Dash(
        __name__, use_pages=True, assets_folder=ASSETS_DIR, server=Flask(__name__)
    )


dash._dash_renderer._set_react_version('18.2.0')
dash_app = init_dash_app()
server = dash_app.server


SESSION_STORE = 'session'
LOCAL_STORE = 'local'
EXAMPLE_STORE = 'example-store-id'

dash_stores = [(DUMMY_OUTPUT, SESSION_STORE),
               (EXAMPLE_STORE, SESSION_STORE)]

ecoact_colors = {'ecoact': ['#DDF5FF',
                            '#81DBFF',
                            '#34C6FF',
                            '#00B3FF',
                            '#009CFF',
                            '#0082DE',
                            '#0066A1',
                            '#005794',
                            '#004576',
                            '#00385F']}


dash_app.layout = dash_base_layout(dash_stores, colors=ecoact_colors)


@callback(Output(NAVBAR_ID, 'children'),
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


if not DASH_APP_SETTINGS.gunicorn_setup:
    dash_app.run_server(
        host='0.0.0.0',
        port=80,
        debug=DEBUG,
        use_reloader=DEBUG if DEBUG is None else False,
    )

if __name__ == '__main__':
    dash_app.run_server(host='0.0.0.0', port=80)
