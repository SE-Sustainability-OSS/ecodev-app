"""
Module containing all project table insertion and deletion methods.
"""
from typing import Any

from ecodev_core import AppUser
from ecodev_core import logger_get
from sqlmodel import Session

from app.db_model.project import Project
from app.db_model.project import ProjectBase
from app.db_model.retrievers.access_retrievers import retrieve_license_rights
from app.db_model.retrievers.access_retrievers import retrieve_project_role
from app.db_model.retrievers.commons import get_user
from app.db_model.retrievers.project_retrievers import retrieve_project_by_id
from app.db_model.retrievers.project_retrievers import verify_project_access
from app.domain_model import ADMIN_ROLES
from app.domain_model.role import Role
from app.pages.module_project.page_rights.methodo.grant_access import grant_user_project_access

log = logger_get(__name__)


def upsert_project(auth: dict | AppUser,
                   project_id: int | None,
                   data: dict[str, Any],
                   session: Session) -> Project | None:
    """
    Upserts a project, depending on whether or not the project already has an id,
    and whether user has relevant rights.
    """
    project = Project(**data)
    project.id = project_id
    if project_id:
        return update_project(project_id, project, session)
    return create_project(auth, project, session)


def create_project(auth: dict | AppUser, project: Project, session: Session) -> Project:
    """
    Creates a new project and adds the creator as OWNER with full project & module access.
    """
    session.add(project)
    session.commit()
    session.refresh(project)

    user = get_user(auth)
    license_rights = retrieve_license_rights(user, session)
    grant_user_project_access(user, project.id, license_rights, Role.OWNER, session)
    return project


def update_project(auth: dict | AppUser,
                   project_id: int | None,
                   project: Project,
                   session: Session) -> Project | None:
    """
    Updates a project, after ensuring user has access rights.
    """
    if not (db_project := retrieve_project_by_id(auth, project_id, session)):
        log.warning(f'Project {project_id} not found')
        return None

    if not verify_project_access(auth, project_id, session):
        log.warning(f'User attempt to edit project {project_id} without access rights.')
        return None

    project_data = project.model_dump(exclude_unset=True)
    db_project.sqlmodel_update(project_data)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


def delete_project(auth: dict | AppUser, project: ProjectBase, session: Session) -> None:
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
