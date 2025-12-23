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
COMM_CHANNEL_URL = 'https://teams.microsoft.com/l/channel/19%3A4e561a8106124325a043fd3ce86acae1%40thread.tacv2/CDA%20Hotline?groupId=53fa0177-24a8-4119-bbce-5410193dc50d&tenantId=6e51e1ad-c54b-4b39-b598-0ffe9ae68fef'  # noqa: E501
FEEDBACK_URL = 'https://forms.office.com/e/UwibxMamt8'
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
VALIDATION_STORE = 'validation-store'
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

# ModuleAccess #
MODULE_NAME = 'module_name'
HAS_ACCESS = 'has_access'
PROJECT_ACCESS_ID = 'project_access_id'


"""
OTHER CALLBACK CONSTANTS
"""
# Custom Callback #
CHECK_ACCESS = 'check_access'
COMPUTATION = 'computation'
MONITORING = 'monitoring'
MONITOR_DETAILS = 'monitor_details'
