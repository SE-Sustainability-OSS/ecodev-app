"""
File containing the app-right's page methodologies to grant (new) user access rights.
NOTE: This file exists to avoid any circular imports between the project module and module.py
I.e. In the module hierarchy, only the Portfolio module is allowed to import all other modules
for this exact purpose of granting module rights in this page.
"""
import re

from ecodev_core import AppUser
from ecodev_core import get_app_services
from ecodev_core import Permission
from sqlmodel import Session

from app.db_model import ProjectAccess
from app.db_model.inserters import upsert_module_access
from app.db_model.inserters import upsert_project_access
from app.db_model.inserters import upsert_user
from app.db_model.retrievers import get_project_users
from app.db_model.retrievers import get_user_by_email
from app.db_model.retrievers import get_users_by_client
from app.domain_model import Role
from app.pages.registry import get_modules


def get_new_project_users(inviting_user: AppUser,
                          emails: list[str],
                          session: Session) -> list[AppUser]:
    """
    For each email, either retrieve existing user or create new user in the database.

    NOTE: For new users, their app-wide license rights (AppRight) are restricted to the
    inviting user's module rights - they cannot elevate a new user beyond their own access.
    """
    return [
        (get_user_by_email(email, session) or _create_new_client_user(inviting_user, email, session))
        for email in emails
    ]


def _create_new_client_user(inviting_user: AppUser, email: str, session: Session) -> AppUser:
    """
    Creates a new user in AppUser and AppRight tables with restricted module rights.

    The new user's app-wide license rights (AppRight) are set to the inviting user's
    module rights, ensuring non-admin users cannot elevate others beyond their own access.

    Client assignment logic:
    - If domains match (both @my-company.com): Use inviting user's client organization
    - If domains differ: Create new client from email domain (jane@another-enterprise.com -> "another-enterprise")

    NOTE: This allows project owners/collaborators to add users to the app, but they
    cannot grant more module rights than they themselves have.
    """
    inviting_user_modules = get_app_services(inviting_user, session)
    invited_user_modules = get_users_by_client(email, session)

    user_module_rights = (inviting_user_modules if not invited_user_modules else
                          [module for module in inviting_user_modules if module in invited_user_modules])

    client = _get_client_from_email(inviting_user, email)
    return upsert_user(email, user_module_rights, session, client)


def _get_client_from_email(inviting_user: AppUser, email: str) -> str:
    """
    Determines the client organization name based on email domains.

    Logic:
    - If inviting user has a client and email domains match: Use inviting user's client
    - Otherwise: Create client name from email domain (e.g., "jane@acme.com" -> "acme")

    NOTE: Compares domain names without .com or .fr suffixes

    Args:
        inviting_user: The user inviting the new user
        email: Email address of the new user

    Returns:
        Client organization name
    """
    invited_domain = email.split('@')[-1].split('.')[0]
    inviting_domain = inviting_user.user.split('@')[-1].split('.')[0]
    if inviting_domain == invited_domain:
        return inviting_user.client

    return invited_domain


def grant_user_project_access(user: AppUser,
                              project_id: int,
                              modules: list[str],
                              role: Role | None,
                              session: Session,
                              inviting_user: AppUser | None = None) -> None:
    """
    Grants the user with project and module access.

    Process:
    1. If user is first on project, assign OWNER role
    2. If user is new to project, assign COLLABORATOR or CLIENT based on permission
    3. Filter modules by intersection of user's app_rights and inviting user's app_rights

    Args:
        user: The user to grant access to
        project_id: The project ID to grant access on
        modules: List of module names to grant access to
        role: Optional role to assign (if None, auto-assigned based on logic)
        inviting_user: The user granting access (used to restrict module rights)
    """

    if not role:
        existing_users = get_project_users(project_id, session)
        if not existing_users:
            role = Role.OWNER
        else:
            role = Role.CLIENT if user.permission == Permission.Client else Role.COLLABORATOR

    access_data = ProjectAccess(
        user_id=user.id,
        role=role,
        project_id=project_id
    )
    project_access = upsert_project_access(project_id, access_data, session)

    filtered_modules = restrict_to_user_module_rights(user, modules, session, inviting_user)
    module_rights = {module.name: bool(module.name in filtered_modules)
                     for module in get_modules()}
    upsert_module_access(module_rights, project_access, session)


def restrict_to_user_module_rights(user: AppUser,
                                   modules: list[str],
                                   session: Session,
                                   inviting_user: AppUser | None = None
                                   ) -> list[str]:
    """
    Filters the list of requested module access with those the user should have access to through
    their app rights / license subscription (if any).

    The filtering is the intersection of:
    - The user being added's app_rights (their license)
    - The inviting user's app_rights (cannot elevate beyond their own rights)

    NOTE: Admin users always have access to all modules.
    NOTE: Expects get_app_services to return enum names (e.g., "PROJECT")
    """
    if user.permission == Permission.ADMIN:
        return [module.name for module in get_modules()]

    if not (user_module_rights := get_app_services(user, session)):
        user_module_rights = (
            get_app_services(client_user_group[0], session)
            if (client_user_group := get_users_by_client(user.client, session))
            else []
        )

    filtered_modules = [module for module in modules if module in user_module_rights]

    if not inviting_user or inviting_user.permission == Permission.ADMIN:
        return filtered_modules

    inviting_user_rights = get_app_services(inviting_user, session)
    if not inviting_user_rights:
        if client_user_group := get_users_by_client(inviting_user.client, session):
            inviting_user_rights = get_app_services(client_user_group[0], session)
        else:
            inviting_user_rights = []

    return [module for module in filtered_modules if module in inviting_user_rights]


def check_email_validity(emails: list[str]) -> list[str]:
    """
    Checks email validity of a list of emails and send an alert if it's the case.
    """
    return [email for email in emails if not validate_email(email)]


def validate_email(email: str) -> bool:
    """
    Validates the format of an email
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return bool(re.match(regex, email))
