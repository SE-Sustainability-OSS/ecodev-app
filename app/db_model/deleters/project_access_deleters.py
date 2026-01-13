"""
Module containing all project access table deletion methods.
"""
from ecodev_core import AppUser
from sqlmodel import Session

from app.db_model.retrievers.access_retrievers import get_project_access


def delete_project_access(user: AppUser,
                          project_id: int,
                          session: Session,
                          ) -> None:
    """
    Deletes the access rights of a user (and associated module accesses) for a given project
    """
    if project_access := get_project_access(user, project_id, session):
        for module in project_access.modules:
            session.delete(module)
        session.delete(project_access)
        session.commit()
    return None
