"""
File containing definition of the module and its pages.
"""
from ecodev_front import icon_navbar
from ecodev_front import Module

from app.pages.module_config.page_comparison.page_comparison import PAGE_COMPARISON
from app.pages.module_config.page_config.page_config import PAGE_CONFIG


MODULE_CONFIG = Module(
    file=__name__,
    name='configuration',
    icon='mdi:cog',
    pages=[
        PAGE_CONFIG,
        PAGE_COMPARISON,
    ],
    navbar_layout=icon_navbar,
    main_page_button_kwargs=dict(label_top='Edit')
)
