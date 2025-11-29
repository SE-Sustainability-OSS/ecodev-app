"""
File containing the user selection component / addition for the add user modal in the page rights.
"""
import dash_mantine_components as dmc
from ecodev_core import AppUser
from ecodev_core import logger_get
from ecodev_front import section_title
from ecodev_front import subtext
from sqlmodel import Session

from app.db_model.retrievers.app_user_retrievers import retrieve_all_users
from app.pages.module_project.page_rights import USERS_MULTISELECT_ID

log = logger_get(__name__)


def email_field(user: AppUser, session: Session) -> dmc.Stack:
    """
    Renders the email field as a tags input component, pre-filled with known colleagues (i.e. user
    which share the same email domain) already registered on the app.
    """
    known_colleagues = [u.user for u in retrieve_all_users(user, session)]
    return dmc.Stack([
        section_title('User email addresses :'),
        subtext('Press Enter to submit an email address not in list.'),
        dmc.TagsInput(
            id=USERS_MULTISELECT_ID,
            placeholder='Search from list or add new email addresses.',
            data=known_colleagues)
    ], gap=3, w='80%')
