"""
File containing methodologies to grant app-wide rights to users (AppRight table).
This is for admin users to manage app-level access, not project-specific access.
"""
import re

from ecodev_core import AppUser
from ecodev_core import Permission
from sqlmodel import Session

from app.db_model.inserters import create_user_credentials
from app.db_model.inserters import update_user_module_rights
from app.db_model.inserters import upsert_user
from app.db_model.retrievers import get_user_by_email


def get_new_app_users(emails: list[str], session: Session) -> list[AppUser]:
    """
    For each email, either retrieve existing user or create new user in the database.
    """
    return [
        (get_user_by_email(email, session) or _create_new_app_user(email, session))
        for email in emails
    ]


def _create_new_app_user(email: str, session: Session) -> AppUser:
    """
    Creates a new user in AppUser table with specified module rights.
    The client is derived from the email domain.
    """
    client = _get_client_from_email(email)
    return upsert_user(email, [], session, client)


def _get_client_from_email(email: str) -> str:
    """
    Determines the client organization name based on email domain.

    Logic: Extract domain from email (e.g., "jane@acme.com" -> "acme")
    """
    return email.split('@')[-1].split('.')[0]


def grant_user_app_rights(user: AppUser | None,
                          modules: list[str],
                          session: Session,
                          permission: Permission | None = None,
                          client: str | None = None,
                          email: str | None = None) -> None:
    """
    Grants the user app-wide module access by updating their AppRight entries.

    Args:
        user: The user to grant access to (None if creating new user)
        modules: List of module names to grant access to
        session: Database session
        permission: Permission level for new users (required if user is None)
        client: Client organization for new users (required if user is None)
        email: Email address for new users (required if user is None)
    """
    if user:
        if permission is not None:
            user.permission = permission
            session.add(user)
        update_user_module_rights(user, modules, session)
    else:
        if permission is None or client is None or email is None:
            raise ValueError('Permission, client, and email are required when creating a new user')
        new_user, password = create_user_credentials(email, permission, session, client)
        update_user_module_rights(new_user, modules, session)


def check_email_validity(emails: list[str]) -> list[str]:
    """
    Checks email validity of a list of emails and returns invalid ones.
    """
    return [email for email in emails if not validate_email(email)]


def validate_email(email: str) -> bool:
    """
    Validates the format of an email
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return bool(re.match(regex, email))
