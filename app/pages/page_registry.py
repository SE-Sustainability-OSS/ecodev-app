"""
File which contains the function instantiating all pages in our app.

It is seperated from the pages and modules to avoid circular imports (as we import our pages
and modules objects across the app) and to ensure that we solely add each page to the registry only
once.
"""
import dash
from ecodev_core import logger_get

from app.pages.module_registry import register_modules
from app.pages.modules import MODULES
from app.pages.page_forbidden.not_forbidden_403 import PAGE_403
from app.pages.page_login.page_login import PAGE_LOGIN
from app.pages.page_main.page_main import PAGE_MAIN
from app.pages.page_not_found.not_found_404 import PAGE_404
from app.pages.pages_account.page_create_user.page_create_user import PAGE_CREATE_USER
from app.pages.pages_account.page_pwd_reset.page_pwd_reset import PAGE_RESET_PWD


log = logger_get(__name__)


def register_pages() -> None:
    """
    Function instantiating / registering all pages in our app with Dash.
    To be called only once post app initialisation (in dash_app.py).
    """
    # Instantiate module registry, used to avoid circular imports across files
    register_modules(MODULES)

    # Register all pages with Dash
    PAGE_LOGIN.register()
    PAGE_MAIN.register()
    PAGE_404.register()
    PAGE_403.register()
    PAGE_RESET_PWD.register()
    PAGE_CREATE_USER.register()

    for module in MODULES:
        for page in module.pages:
            page.register()

    log.info('The following pages have been registered:')
    log.info([x['path'] for x in dash.page_registry.values()])
