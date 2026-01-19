"""
File containing AppUser inserters.
"""
import random

from ecodev_core import AppRight
from ecodev_core import AppUser
from ecodev_core import logger_get
from ecodev_core import Permission
from ecodev_core.authentication import _hash_password
from sqlmodel import Session

from app.constants import PASSWORD_LENGTH
from app.constants import PWD_CHAR_CHOICES
from app.db_model.retrievers.app_user_retrievers import get_user_by_email

log = logger_get(__name__)


def create_user_credentials(email: str,
                            permission: Permission,
                            session: Session,
                            client: str = '') -> tuple[AppUser, str]:
    """
    Create user, auto-generated password and hashed-password.
    """
    password = ''.join(random.choice(PWD_CHAR_CHOICES) for i in range(PASSWORD_LENGTH))
    user = AppUser(user=email,
                   password=_hash_password(password),
                   permission=permission,
                   client=client)
    session.add(user)
    session.flush()
    session.refresh(user)
    return user, password


def update_user_module_rights(client: AppUser, modules: list[str], session: Session) -> None:
    """
    Update the client's module rights in the database.
    NOTE: Only use for external users, as internal users are managed through the eco-auth service.
    NOTE: Using the AppRight table instead of the ModuleAccess table, as the former will restrict
    module usage throughout the app (including when providing rights to other users), while the
    latter restricts user module access on a per-portfolio basis.
    """
    if client.rights:
        for right in client.rights:
            session.delete(right)

    for module in modules:
        session.add(AppRight(user_id=client.id, app_service=module))
    session.commit()
    return


def upsert_user(email: str,
                app_rights: list[str],
                session: Session,
                client: str = '',
                permission: Permission = Permission.USER
                ) -> AppUser:
    """
    Upserts a user and its module rights in the database.

    Args:
        email: User's email address
        app_rights: List of module rights to grant
        session: Database session
        client: Optional client name to associate with the user
    TODO: Add permission input parameter.
    TODO: Update so that user app access and project access are de-coupled.
          Users will only be able to add users to their projects if they already have access to the app.
    """
    try:
        if not (user := get_user_by_email(email, session)):
            user, password = create_user_credentials(email, permission, session, client)
        update_user_module_rights(user, app_rights, session)
        return user
    except Exception as e:
        log.error(f'Error upserting user {email}: {e}')
        raise e


def add_user(user_id: int, email: str, hashed_password: str, session: Session) -> None:
    """
    Adds a user to the database
    """
    session.add(AppUser(id=user_id,
                        user=email,
                        password=hashed_password,
                        permission=Permission.USER))
    session.commit()
