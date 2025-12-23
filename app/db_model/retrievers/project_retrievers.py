"""
Module containing all Project retrievers
"""
from ecodev_core import AppUser
from ecodev_core import logger_get
from ecodev_core import Permission
from sqlmodel import select
from sqlmodel import Session

from app.db_model.project import Project
from app.db_model.project_access import ProjectAccess
from app.db_model.retrievers.commons import get_user

log = logger_get(__name__)


def retrieve_all_projects(auth: dict | AppUser, session: Session) -> list[Project]:
    """
    Retrieves all projects - To be used for project access management only.
    """
    if get_user(auth).permission is Permission.ADMIN:
        return session.exec(select(Project)).all()
    return retrieve_user_projects(auth, Project, session)


def retrieve_user_projects(auth: dict | AppUser,
                           session: Session) -> list[Project]:
    """
    Retrieves all projects accessible by the user / token.
    """
    return list(session.exec(select(Project)
                             .join(ProjectAccess, isouter=True)
                             .where(ProjectAccess.user_id == get_user(auth).id)
                             ).unique())


def retrieve_project_by_id(auth: dict | AppUser,
                           project_id: int,
                           session: Session
                           ) -> Project | None:
    """
    Attempts to retrieve a project for the given id, and checks for user access rights.
    If found, returns the project requested.
    """
    return session.exec(select(Project)
                        .join(ProjectAccess, isouter=True)
                        .where(Project.id == project_id,
                               ProjectAccess.user_id == get_user(auth).id)
                        ).first()


def verify_project_access(token: dict,
                          project_id: int,
                          session: Session) -> bool:
    """
    Verifies that the user is allowed to interact with the project
    """
    project_ids = [p.id for p in retrieve_user_projects(token, session)]
    return True if project_id in project_ids else False
