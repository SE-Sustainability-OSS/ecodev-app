"""
Module creating / instantiating the dash app
"""
import dash
from dash import Dash
from ecodev_core import create_db_and_tables
from ecodev_core import engine
from ecodev_core import logger_get
from ecodev_core import SETTINGS
from ecodev_core import upsert_app_users
from ecodev_front import dash_base_layout
from flask import Flask
from sqlmodel import Session

import app.db_model as db_model
from app.constants import ASSETS_DIR
from app.constants import DATA_DIR
from app.domain_model.dmc_theme import DMC_THEME
from app.pages.common.stores import STORES
from app.pages.page_registry import register_pages


log = logger_get(__name__)


def init_dash_app() -> Dash:
    """
    Initialize the dash application, running all what need to be run before startup.
    """
    log.info('Initializing dash app')
    create_db_and_tables(db_model.AppUser)

    if (file_path := DATA_DIR / 'users.json').exists():
        with Session(engine) as session:
            upsert_app_users(file_path, session)

    dash._dash_renderer._set_react_version('18.2.0')

    dash_app = Dash(
        __name__,
        server=Flask(__name__),
        use_pages=True,
        assets_folder=ASSETS_DIR,
        suppress_callback_exceptions=True,
    )

    dash_app.layout = dash_base_layout(stores=STORES, theme=DMC_THEME)

    register_pages()

    return dash_app


DASH_APP = init_dash_app()

# Required for gunicorn setup
server = DASH_APP.server

if not SETTINGS.dash_settings.gunicorn_setup:
    DASH_APP.run(
        host='0.0.0.0',
        port=80,
        debug=SETTINGS.dash_settings.debug,
        use_reloader=debug if (debug := SETTINGS.dash_settings.debug) is None else False,
    )


if __name__ == '__main__':
    DASH_APP.run(host='0.0.0.0', port=80)
