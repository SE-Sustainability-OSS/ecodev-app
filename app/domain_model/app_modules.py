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
    PROJECT = 'Project'
    CONFIG = 'Configuration'
    DASHBOARD = 'Dashboard'
    STYLE_GUIDE = 'Style-Guide'


ALL_MODULE_NAMES = [module.value for module in AppModule]
