"""
Global useful constants
"""
import string
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class AppNameSettings(BaseSettings):
    """
    Settings class to control the app name.
    """

    app_name: str = ''
    model_config = SettingsConfigDict(env_file='.env')


APP_NAME = AppNameSettings().app_name

"""
PAGE & NAVIGATION CONSTANTS
"""
DUMMY_OUTPUT = 'dummy-output'
DATA_DIR = Path('/app/data')
ASSETS_DIR = Path('/app/app/assets')
COMM_CHANNEL_URL = 'https://teams.microsoft.com'


FEEDBACK_URL = 'https://forms.office.com'

PWD_CHAR_CHOICES = string.ascii_letters + string.digits + '!?.,;@#~][+=-/*()&^%$'
PASSWORD_LENGTH = 15
