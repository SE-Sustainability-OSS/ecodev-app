"""
Global useful constants
"""
import string
from pathlib import Path

from ecodev_core import SETTINGS


APP_NAME = SETTINGS.app_name

"""
PATH VARIABLES
"""
DATA_DIR = Path('/app/data')
ASSETS_DIR = Path('/app/app/assets')


"""
MAIN URL CONSTANTS
"""
MAIN_PAGE_URL = '/'

"""
LINKS CONSTANTS
"""
COMM_CHANNEL_URL = 'https://ecosia.com'
FEEDBACK_URL = 'https://ecosia.com'
DOCUMENTATION_URL = 'https://ecosia.com'


"""
SECURITY CONSTANTS
"""
PWD_CHAR_CHOICES = string.ascii_letters + string.digits + '!?.,;@#~][+=-/*()&^%$'
PASSWORD_LENGTH = 15


"""
DASH DATA STORES
"""
ALERT_STORE = 'alert-store'
PROJECT_ID_STORE = 'project-id-store'
USER_DELETION_STORE = 'user-deletion-store'


"""
ACCESS CONSTANTS
"""
PROJECT = 'project'
CREATE_PROJECT = 'create_project'

# Project #
NAME = 'name'
DESCRIPTION = 'description'
PROJECT_ID = 'project_id'
YEAR = 'year'
MODIFIED_BY = 'modified_by'
DEMO = 'demo'

# ProjectAccess #
USER_ID = 'user_id'
ROLE = 'role'
IS_PM = 'is_pm'
USER = 'user'
MODULE = 'module'

# ModuleAccess #
MODULE_ACCESS = 'module_access'
MODULE_NAME = 'module_name'
HAS_ACCESS = 'has_access'
PROJECT_ACCESS_ID = 'project_access_id'


"""
OTHER CALLBACK CONSTANTS
"""
# Custom Callback #
CHECKS = 'checks'
COMPUTATION = 'computation'
MONITORING = 'monitoring'
MONITOR_DETAILS = 'monitor_details'
