"""
File containing definition of the module and its pages.
"""
from ecodev_front import icon_navbar
from ecodev_front import Module

from app.domain_model import AppModule
from app.domain_model.color_utils import get_color
from app.pages.module_project.page_info.page_info import PAGE_INFO
from app.pages.module_project.page_rights.page_rights import PAGE_RIGHTS

MODULE_PROJECT = Module(
    file=__name__,
    name=AppModule.PROJECT.value,
    icon='fluent-mdl2:new-team-project',
    pages=[
        PAGE_INFO,
        PAGE_RIGHTS
    ],
    navbar_layout=icon_navbar,
    main_page_button_kwargs=dict(label_top='Update',
                                 label_bottom='Project & Rights',
                                 color=get_color('blue.4'))
)
