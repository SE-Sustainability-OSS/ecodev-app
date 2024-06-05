"""
Module listing all public method from the components modules.

You should put here all components expected to be used in several pages
"""
from app.components.footer import app_footer
from app.components.page_helpers import generic_page
from app.components.user_components import USER_COMPONENTS

__all__ = ['app_footer', 'USER_COMPONENTS', 'generic_page']
