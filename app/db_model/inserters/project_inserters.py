"""
Module containing all project table insertion and deletion methods.
"""
from ecodev_core import AppUser
from ecodev_core import logger_get
from sqlmodel import Session

from app.db_model.project import Project
from app.db_model.project import ProjectBase
from app.db_model.project import ProjectCreate
from app.db_model.project import ProjectPublic
from app.db_model.project import ProjectUpdate
from app.db_model.retrievers.access_retrievers import retrieve_project_role
from app.db_model.retrievers.commons import get_user
from app.domain_model import ADMIN_ROLES
# from app.db_model.inserters.project_access_inserters import create_project_access

log = logger_get(__name__)


def upsert_project(auth: dict | AppUser,
                   project: ProjectCreate | ProjectUpdate,
                   session: Session) -> ProjectPublic:
    """
    Upserts a project, depending on whether or not the project already has an id.
    """
    if isinstance(project, ProjectUpdate) and project.id:
        return update_project(project.id, project, session)
    return create_project(auth, project, session)


def create_project(auth: dict | AppUser, project: ProjectCreate, session: Session) -> ProjectPublic:
    """
    Creates a new project.
    """
    project = Project(**project.model_dump())
    session.add(project)
    session.commit()
    session.refresh(project)
    # create_project_access(AppUser, project.id, session)
    return project


def update_project(project_id: int | None, project: ProjectUpdate, session: Session) -> ProjectPublic:
    """
    Updates a project.
    """
    if not (db_project := session.get(Project, project_id)):
        log.warning(f'Project {project_id} not found')
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
