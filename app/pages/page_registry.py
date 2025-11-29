"""
File which contains the function instantiating all pages in our app.

It is seperated from the pages and modules to avoid circular imports (as we import our pages
and modules objects across the app) and to ensure that we solely add each page to the registry only
once.
"""
import dash
from ecodev_core import logger_get

from app.pages.modules import MODULES
from app.pages.page_forbidden.not_forbidden_403 import PAGE_403
from app.pages.page_login.page_login import PAGE_LOGIN
from app.pages.page_main.page_main import PAGE_MAIN
from app.pages.page_not_found.not_found_404 import PAGE_404


log = logger_get(__name__)


def register_pages() -> None:
    """
    Function instantiating / registering all pages in our app with Dash.
    To be called only once post app initialisation (in dash_app.py).
    """
    PAGE_LOGIN.register()
    PAGE_MAIN.register()
    PAGE_404.register()
    PAGE_403.register()

    for module in MODULES:
        for page in module.pages:
            page.register()

    log.info('The following pages have been registered:')
    log.info([x['path'] for x in dash.page_registry.values()])
