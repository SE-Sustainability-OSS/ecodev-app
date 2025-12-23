"""
Module listing all public method from the components modules.

You should put here all components expected to be used in several pages
"""
from app.pages.common.app_access import user_login
from app.pages.common.app_access import user_logout
from app.pages.common.app_access import verify_page_access
from app.pages.common.asides import show_asides
from app.pages.common.custom_callback import safe_callback
from app.pages.common.footer import main_footer
from app.pages.common.navbar import show_navbar
from app.pages.common.stores import STORES

__all__ = ['user_login', 'user_logout', 'verify_page_access', 'STORES',
           'main_footer', 'show_navbar', 'show_asides', 'safe_callback']
