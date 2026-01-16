"""
Module containing all project table insertion and deletion methods.
"""
from typing import Any

from ecodev_core import AppUser
from ecodev_core import logger_get
from sqlmodel import Session

from app.db_model.project import Project
from app.db_model.retrievers import get_app_rights
from app.db_model.retrievers import get_auth_user
from app.db_model.retrievers import get_project_by_id
from app.db_model.retrievers import verify_project_access
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
        return update_project(auth, project_id, project, session)
    return create_project(auth, project, session)


def create_project(auth: dict | AppUser, project: Project, session: Session) -> Project:
    """
    Creates a new project and adds the creator as OWNER with full project & module access.
    """
    session.add(project)
    session.commit()
    session.refresh(project)

    user = get_auth_user(auth)
    app_rights = [module.name for module in get_app_rights(user, session)]
    grant_user_project_access(user, project.id, app_rights, Role.OWNER, session)
    return project


def update_project(auth: dict | AppUser,
                   project_id: int | None,
                   project: Project,
                   session: Session) -> Project | None:
    """
    Updates a project, after ensuring user has access rights.

    NOTE: Prior to updating the db_project object, we firstly remove any empty values from the Project object provided,
    with project.model_dump(exclude_unset=True). This ensures we only update the fields that have been changed,
    and not overwrite the existing values with None.
    """
    if not (db_project := get_project_by_id(auth, project_id, session)):
        log.warning(f'Project {project_id} not found')
        return None

    if not verify_project_access(auth, project_id, session):
        log.warning(f'User attempt to edit project {project_id} without access rights.')
        return None
    project_data = project.model_dump(exclude_unset=True)
    db_project.sqlmodel_update(project_data)
    session.commit()
    session.refresh(db_project)
    return db_project
