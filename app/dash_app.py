"""
Module creating / instantiating the dash app
"""
import dash
from asgiref.wsgi import WsgiToAsgi
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
from app.pages.modules import MODULES
from app.pages.page_forbidden.page_forbidden_403 import PAGE_403
from app.pages.page_login.page_login import PAGE_LOGIN
from app.pages.page_main.page_main import PAGE_MAIN
from app.pages.page_not_found.page_not_found_404 import PAGE_404
from app.pages.pages_account.page_manage_user.page_manage_user import PAGE_MANAGE_USERS
from app.pages.pages_account.page_pwd_reset.page_pwd_reset import PAGE_RESET_PWD
from app.pages.registry import add_modules_to_registry
from app.pages.registry import add_pages_to_registry


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

    _register_dash_pages()

    return dash_app


def _register_dash_pages() -> None:
    """
    Function instantiating / registering all pages in our app with Dash.
    To be called only once post app initialisation (in dash_app.py).
    """
    pages = [
        PAGE_LOGIN,
        PAGE_MAIN,
        PAGE_404,
        PAGE_403,
        PAGE_RESET_PWD,
        PAGE_MANAGE_USERS,
    ] + [page for module in MODULES for page in module.pages]

    # Add pages and modules to registry
    add_pages_to_registry(pages)
    add_modules_to_registry(MODULES)

    # Register all pages with Dash
    for page in pages:
        page.register()

    log.info('The following pages have been registered:')
    log.info([x['path'] for x in dash.page_registry.values()])


DASH_APP = init_dash_app()
server = WsgiToAsgi(DASH_APP.server)

if not SETTINGS.dash_settings.gunicorn_setup:
    DASH_APP.enable_dev_tools(
        dev_tools_ui=SETTINGS.dash_settings.debug,
        dev_tools_props_check=SETTINGS.dash_settings.debug,
        dev_tools_hot_reload=SETTINGS.dash_settings.debug,
    )


if __name__ == '__main__':
    DASH_APP.run(host='0.0.0.0', port=80)
