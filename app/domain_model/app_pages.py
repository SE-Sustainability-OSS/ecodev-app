"""
List of the app's modules
"""
from enum import Enum
from enum import unique

from app.domain_model import AppModule


@unique
class AppPage(str, Enum):
    """
    List of the app's pages
    """
    PROJECT = 'Project'
    CONFIG = 'Configuration'
    DASHBOARD = 'Dashboard'
    STYLE_GUIDE = 'Style-Guide'


ALL_MODULE_NAMES = [module.value for module in AppModule]
