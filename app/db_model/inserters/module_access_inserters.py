"""
Module containing all module access table insertion and deletion methods.
"""
from sqlmodel import Session

from app.constants import HAS_ACCESS
from app.constants import MODULE_NAME
from app.constants import PROJECT_ACCESS_ID
from app.db_model.inserters.commons import upsert_dict
from app.db_model.module_access import ModuleAccess
from app.db_model.project_access import ProjectAccess
from app.db_model.retrievers.access_retrievers import get_app_rights
from app.db_model.retrievers.app_user_retrievers import get_user_by_id
from app.domain_model import AppModule


def upsert_module_access(module_rights: dict[str, bool] | None,
                         project_access: ProjectAccess,
                         session: Session
                         ) -> None:
    """
    Upserts module access rights for a given user.

    NOTE: If no module rights are provided, the user's license rights are retrieved from the database.
    """
    if not module_rights:
        user = get_user_by_id(project_access.user_id, session)
        license_rights = get_app_rights(user, session)
        module_rights = {module.name: bool(module in license_rights) for module in AppModule}

    for module_name, has_access in module_rights.items():
        upsert_dict(ModuleAccess,
                    {MODULE_NAME: module_name,
                     HAS_ACCESS: has_access,
                     PROJECT_ACCESS_ID: project_access.id},
                    session,
                    )
