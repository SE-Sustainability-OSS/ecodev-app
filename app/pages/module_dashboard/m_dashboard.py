"""
File containing definition of the module and its pages.
"""
from ecodev_front import icon_navbar
from ecodev_front import Module

from app.domain_model import AppModule
from app.domain_model.color_utils import get_color
from app.pages.module_dashboard.page_kpi.page_kpi import PAGE_KPI
from app.pages.module_dashboard.page_report.page_report import PAGE_REPORT

MODULE_DASHBOARD = Module(
    file=__name__,
    name=AppModule.DASHBOARD.value,
    icon='carbon:dashboard-reference',
    pages=[
        PAGE_REPORT,
        PAGE_KPI,
    ],
    navbar_layout=icon_navbar,
    main_page_button_kwargs=dict(color=get_color('green.5'))
)
