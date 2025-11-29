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
from ecodev_core import Permission
from sqlmodel import Session

from app.constants import ROLE
from app.constants import USER
from app.constants import USER_ID
from app.db_model.inserters.app_user_inserters import upsert_user
from app.db_model.inserters.project_access_inserters import upsert_project_access
from app.db_model.retrievers.app_user_retrievers import retrieve_all_users
from app.db_model.retrievers.app_user_retrievers import retrieve_user_by_email
from app.domain_model import Role
from app.pages.module_config.m_config import MODULE_CONFIG
from app.pages.module_dashboard.m_dashboard import MODULE_DASHBOARD
from app.pages.module_style_guide.m_style_guide import MODULE_STYLE_GUIDE


MODULES = [
    MODULE_CONFIG,
    MODULE_DASHBOARD,
    MODULE_STYLE_GUIDE,
]


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
    If user is not found in local db, nor in eco-auth, add user as a client, retrieve inviting
    user's module rights and pass them onto invitee.

    TODO-B: Edge-case to fix, in case consultant adds new client with modules outside of license
    for organisation. This will copy the consultant's module rights instead. To be fixed with the
    License table.
    """
    user_module_rights = get_app_services(inviting_user, session)
    return upsert_user(email, user_module_rights, session)


def grant_user_project_access(user: AppUser,
                              project_id: int,
                              modules: list[str],
                              session: Session) -> None:
    """
    Grants the user with project and module access.
    If user is internal, grant access to all modules, else restrict to list of modules provided
    (which is equivalent or sub-portion of modules the user adding these rights has).
    """
    modules = restrict_external_module_access(user, modules, session)
    module_data = ({module.name: module.name in modules for module in MODULES}
                   if user.permission == Permission.Client else
                   {module.name: True for module in MODULES})

    pft_access = {
        USER_ID: user.id,
        USER: user.user,
        ROLE: Role.CLIENT if user.permission == Permission.Client else Role.CONSULTANT,
        project_id: project_id,
    } | module_data

    upsert_project_access(project_id, pft_access, MODULES, session)


def restrict_external_module_access(user: AppUser,
                                    modules: list[str],
                                    session: Session) -> list[str]:
    """
    Filters the list of requested module access with those the client has access to through their
    app rights / license subscription.
    NOTE: If an external adds another user, they cannot share modules they do not have access to,
    so this filter is only really relevant in case an internal adds an external user
    """
    if user.permission != Permission.Client:
        return modules
    if user_license_modules := get_app_services(user, session):
        return [module for module in modules if module in user_license_modules]
    if colleague := retrieve_all_users(user, session):
        return [module for module in modules if module in get_app_services(colleague[0], session)]
    return modules


def check_email_validity(emails: list[str], user: AppUser) -> dmc.Alert | None:
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
