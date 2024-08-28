"""
Module creating the app_template tool dash app
"""
import dash
from dash import Dash
from ecodev_core import create_db_and_tables
from ecodev_core import engine
from ecodev_core import logger_get
from ecodev_core import upsert_app_users
from ecodev_front import dash_base_layout
from flask import Flask
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from sqlmodel import Session

import app.db_model as db_model
from app.constants import APP_COLORS
from app.constants import ASSETS_DIR
from app.constants import DATA_DIR


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


EXAMPLE_STORE = 'example-store-id'
dash_stores = [(EXAMPLE_STORE, 'session')]

dash_app.layout = dash_base_layout(dash_stores, colors=APP_COLORS)


if not DASH_APP_SETTINGS.gunicorn_setup:
    dash_app.run_server(
        host='0.0.0.0',
        port=80,
        debug=DEBUG,
        use_reloader=DEBUG if DEBUG is None else False,
    )

if __name__ == '__main__':
    dash_app.run_server(host='0.0.0.0', port=80)
