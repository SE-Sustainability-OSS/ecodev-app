"""
List of the app's modules
"""
from enum import Enum
from enum import unique


@unique
class AppModule(str, Enum):
    """
    List of the app's modules
    """
    PROJECT = 'project'
    CONFIG = 'configuration'
    DASHBOARD = 'dashboard'
    STYLE_GUIDE = 'style-guide'


ALL_MODULE_NAMES = [module.name for module in AppModule]
