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
PATH VARIABLES
"""
DATA_DIR = Path('/app/data')
ASSETS_DIR = Path('/app/app/assets')


"""
ADMIN CONSTANTS
"""
COMM_CHANNEL_URL = 'https://teams.microsoft.com'
FEEDBACK_URL = 'https://forms.office.com'
PWD_CHAR_CHOICES = string.ascii_letters + string.digits + '!?.,;@#~][+=-/*()&^%$'
PASSWORD_LENGTH = 15


"""
APP COLORS
"""
COLORS_ID = 'global_colors'
APP_COLORS = {COLORS_ID: ['#DDF5FF',
                          '#81DBFF',
                          '#34C6FF',
                          '#00B3FF',
                          '#009CFF',
                          '#0082DE',
                          '#0066A1',
                          '#005794',
                          '#004576',
                          '#00385F']}
