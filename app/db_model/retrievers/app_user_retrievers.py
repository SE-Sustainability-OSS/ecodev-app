"""
Module containing all app user retrievers.
"""
from ecodev_core import AppUser
from sqlmodel import select
from sqlmodel import Session


def get_user_by_id(user_id: int, session: Session) -> AppUser | None:
    """
    Retrieves a user from the database by their ID.
    """
    return session.exec(select(AppUser).where(AppUser.id == user_id)).first()


def get_user_by_email(email: str, session: Session) -> AppUser | None:
    """
    Find user by email in the database.
    """
    return session.exec(select(AppUser).where(AppUser.user == email)).first()


def get_all_users(session: Session) -> list[AppUser]:
    """
    Retrieves a list of all users
    """
    return session.exec(select(AppUser)).all()


def get_users_by_client(client: str, session: Session) -> list[AppUser]:
    """
    Retrieves a list of users with the same 'client' attribute of the AppUser table.
    NOTE: 'client' can be thought of as grouping of users (e.g. users from the same organisation).
    """
    return session.exec(select(AppUser)
                        .where(AppUser.client == client)
                        ).all()
