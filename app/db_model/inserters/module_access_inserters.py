"""
Module containing all module access table insertion and deletion methods.
"""
from ecodev_core import logger_get
from sqlmodel import Session

from app.constants import HAS_ACCESS
from app.constants import MODULE_NAME
from app.constants import PROJECT_ACCESS_ID
from app.db_model.inserters.commons import upsert_dict
from app.db_model.module_access import ModuleAccess
from app.db_model.project_access import ProjectAccess
from app.db_model.retrievers.access_retrievers import retrieve_license_rights
from app.db_model.retrievers.app_user_retrievers import retrieve_user_by_id
from app.domain_model import AppModule

log = logger_get(__name__)


def upsert_module_access(module_rights: dict[str, bool] | None,
                         project_access: ProjectAccess,
                         session: Session
                         ) -> None:
    """
    Upserts module access rights for a given user.

    NOTE: If no module rights are provided, the user's license rights are retrieved from the database.
    """
    if not module_rights:
        user = retrieve_user_by_id(project_access.user_id, session)
        license_rights = retrieve_license_rights(user, session)
        module_rights = {module.value: bool(module in license_rights) for module in AppModule}

    for module_name, has_access in module_rights.items():
        upsert_dict(ModuleAccess,
                    {MODULE_NAME: module_name,
                     HAS_ACCESS: has_access,
                     PROJECT_ACCESS_ID: project_access.id},
                    session,
                    )
    return None
