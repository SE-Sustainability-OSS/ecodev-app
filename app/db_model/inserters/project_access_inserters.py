"""
Module containing all project access table insertion and deletion methods.
"""
from ecodev_core import AppUser
from ecodev_core import logger_get
from sqlmodel import Session

from app.db_model.inserters.commons import upsert_dict
from app.db_model.project_access import ProjectAccess
from app.db_model.retrievers.access_retrievers import get_project_access

log = logger_get(__name__)


def upsert_project_access(project_id: int,
                          project_access: ProjectAccess,
                          session: Session,
                          ) -> ProjectAccess:
    """
    Creates mew / Updates project access record and upserts the module access rights.
    """
    project_access = upsert_dict(
        ProjectAccess,
        project_access.model_dump(exclude_unset=True),
        session
    )
    log.info(f'User #{project_access.user_id} now has {project_access.role} access '
             f'rights on project {project_id}')
    session.refresh(project_access)
    return project_access


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
