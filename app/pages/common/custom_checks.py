"""
File containing custom checks to be used in the custom callback decorator.
NOTE: Due to the way it is currently implemented, each checks below are given
the token, project_id and session as arguments.
"""
from ecodev_core import Permission
from ecodev_core import safe_get_user
from sqlmodel import Session

from app.db_model.retrievers.project_retrievers import get_user_projects


def verify_token(token: dict, project_id: int, session: Session) -> bool:
    """
    Verifies that the token is valid.
    NOTE: This is the default check run by the safe_callback decorator.
    """
    return True if safe_get_user(token) else False


def verify_admin(token: dict, project_id: int, session: Session) -> bool:
    """
    Verifies that the user is an admin
    """
    return True if safe_get_user(token).permission == Permission.ADMIN else False


def verify_project_access(token: dict,
                          project_id: int,
                          session: Session) -> bool:
    """
    Verifies that the user is allowed to interact with the project
    """
    project_ids = [p.id for p in get_user_projects(token, session)]
    return True if project_id in project_ids else False
