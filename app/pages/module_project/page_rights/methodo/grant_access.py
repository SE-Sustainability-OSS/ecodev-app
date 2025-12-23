"""
File containing the app-right's page methodologies to grant (new) user access rights.
NOTE: This file exists to avoid any circular imports between the project module and module.py
I.e. In the module hierarchy, only the Portfolio module is allowed to import all other modules
for this exact purpose of granting module rights in this page.
"""
import re

import dash_mantine_components as dmc
from ecodev_core import AppUser
from ecodev_core import get_app_services
from ecodev_core import logger_get
from ecodev_core import Permission
from sqlmodel import Session

from app.db_model.inserters.app_user_inserters import upsert_user
from app.db_model.inserters.project_access_inserters import upsert_project_access
from app.db_model.retrievers.app_user_retrievers import retrieve_user_by_email
from app.db_model.retrievers.app_user_retrievers import retrieve_users_by_client
from app.domain_model import ALL_MODULE_NAMES
from app.domain_model import ProjectAccessData
from app.domain_model import Role

log = logger_get(__name__)


def get_new_project_users(user: AppUser,
                          emails: str,
                          session: Session) -> list[AppUser]:
    """
    For each email, either create new (external) user or retrieve from db if app access already
    granted.
    NOTE: For new client users, retrieve inviting user's module rights and pass them onto invitee.
    NOTE: For consultants on eco-auth, but not yet registered within the app, we recreate an
    AppUser instance, for the purpose of adding their project & module access (done in later stage)
    """
    return [
        (retrieve_user_by_email(email, session) or _create_new_client_user(user, email, session))
        for email in emails
    ]


def _create_new_client_user(inviting_user: AppUser, email: str, session: Session):
    """
    If user is not found in local db, add user as a client with module rights being the
    intersection of:
    - The inviting user's module rights (what they can share)
    - The invited user's license rights from eco-auth (what they're entitled to)

    This ensures users only get modules they're both entitled to AND that the inviter can share.
    """
    inviting_user_modules = get_app_services(inviting_user, session)
    invited_user_modules = retrieve_users_by_client(email, session)

    # Grant the intersection: smallest set of modules between inviter rights and invitee license
    if invited_user_modules:
        user_module_rights = [module for module in inviting_user_modules
                              if module in invited_user_modules]
    else:
        # If invited user has no license in eco-auth, fall back to inviter's modules
        user_module_rights = inviting_user_modules

    return upsert_user(email, user_module_rights, session)


def grant_user_project_access(user: AppUser,
                              project_id: int,
                              modules: list[str],
                              role: Role,
                              session: Session) -> None:
    """
    Grants the user with project and module access.
    If user is internal, grant access to all modules, else restrict to list of modules provided
    (which is equivalent or sub-portion of modules the user adding these rights has).
    """
    filtered_modules = restrict_to_user_module_rights(user, modules, session)
    module_access = {module: bool(module in filtered_modules) for module in ALL_MODULE_NAMES}

    access_data = ProjectAccessData(
        user_id=user.id,
        role=role,
        project_id=project_id,
        module_access=module_access,
    )
    upsert_project_access(project_id, access_data, session)


def restrict_to_user_module_rights(user: AppUser,
                                   modules: list[str],
                                   session: Session,
                                   ) -> list[str]:
    """
    Filters the list of requested module access with those the user should have access to through
    their app rights / license subscription (if any).
    NOTE: Admin users always have access to all modules.
    NOTE: If an external adds another user, they cannot share modules they do not have access to,
    so this filter is only really relevant in case an internal adds an external user.
    """
    if user.permission == Permission.ADMIN:
        return ALL_MODULE_NAMES
    if user_license_modules := get_app_services(user, session):
        return [module for module in modules if module in user_license_modules]
    if client_user_group := retrieve_users_by_client(user.client, session):
        return [module for module in modules
                if module in get_app_services(client_user_group[0], session)]
    return modules


def check_email_validity(emails: list[str]) -> dmc.Alert | None:
    """
    Checks email validity of a list of emails and send an alert if it's the case.
    """
    alerts = []
    if invalid_emails := {email for email in emails if not validate_email(email)}:
        alerts.extend([dmc.Text(email, ta='center') for email in invalid_emails])

    return None if not alerts else dmc.Alert(alerts, title='Incorrect emails:', color='red')


def validate_email(email: str) -> bool:
    """
    Validates the format of an email
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return bool(re.match(regex, email))
