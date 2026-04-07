"""
Module listing all public method from the components modules.

You should put here all components expected to be used in several pages
"""
from app.pages.common.footer import main_footer
from app.pages.common.header import display_app_header
from app.pages.common.stores import STORES

__all__ = ['STORES', 'main_footer', 'display_app_header']
