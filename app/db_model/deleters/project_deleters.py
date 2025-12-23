"""
Module containing all project table deletion methods.
"""
from ecodev_core import AppUser
from ecodev_core import logger_get
from sqlmodel import Session

from app.db_model.project import Project
from app.db_model.retrievers.access_retrievers import retrieve_project_role
from app.db_model.retrievers.commons import get_user
from app.domain_model import ADMIN_ROLES

log = logger_get(__name__)


def delete_project(auth: dict | AppUser, project: Project, session: Session) -> None:
    """
    Deletes a project, after checking that the user is allowed to delete the project.
    """
    user = get_user(auth)

    if not ((role := retrieve_project_role(user, project.id, session)) in ADMIN_ROLES):
        log.warning(f'{user} ({role}) does not have permissions to delete project {project.id}')
        return None

    for user_access in project.users:
        for module_access in user_access.modules:
            session.delete(module_access)
        session.delete(user_access)

    for computation in project.computations:
        session.delete(computation)
    session.delete(project)
    session.commit()

    log.info(f'Project {project.name} (id: {project.id}) deleted!')
    return None
