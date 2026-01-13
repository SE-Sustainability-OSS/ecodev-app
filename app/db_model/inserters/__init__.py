"""
This is the recoupment of modules where to implement all db insertions.
"""
from app.db_model.inserters.app_user_inserters import upsert_user
from app.db_model.inserters.computation_inserters import create_update_computation
from app.db_model.inserters.module_access_inserters import upsert_module_access
from app.db_model.inserters.project_access_inserters import upsert_project_access
from app.db_model.inserters.project_inserters import upsert_project

__all__ = [
    'upsert_project',
    'upsert_project_access',
    'upsert_module_access',
    'upsert_user',
    'create_update_computation',
]
