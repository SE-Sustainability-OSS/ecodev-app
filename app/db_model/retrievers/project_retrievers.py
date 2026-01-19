"""
Module containing all Project retrievers
"""
from ecodev_core import AppUser
from ecodev_core import Permission
from sqlmodel import select
from sqlmodel import Session

from app.db_model.project import Project
from app.db_model.project_access import ProjectAccess
from app.db_model.retrievers.commons import get_auth_user


def get_user_projects(auth: dict | AppUser,
                      session: Session) -> list[Project]:
    """
    Retrieves all projects accessible by the user / token.
    NOTE: Exception made for admin users, who can access all projects.
    """
    if (user := get_auth_user(auth)).permission == Permission.ADMIN:
        return session.exec(select(Project)).all()

    return list(session.exec(select(Project)
                             .join(ProjectAccess, isouter=True)
                             .where(ProjectAccess.user_id == user.id)
                             ).unique())


def get_project_by_id(auth: dict | AppUser,
                      project_id: int,
                      session: Session
                      ) -> Project:
    """
    Attempts to retrieve a project for the given id, and checks for user access rights.
    If found, returns the project requested.
    NOTE: Exception made for admin users, who can access all projects.
    """
    if (user := get_auth_user(auth)).permission == Permission.ADMIN:
        return session.exec(select(Project).where(Project.id == project_id)).first()

    return session.exec(select(Project)
                        .join(ProjectAccess, isouter=True)
                        .where(Project.id == project_id,
                               ProjectAccess.user_id == user.id)
                        ).first()
