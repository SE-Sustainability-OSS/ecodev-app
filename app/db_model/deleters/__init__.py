"""
This is the recoupment of modules where to implement all db deletions.
"""
from app.db_model.deleters.project_deleters import delete_project

__all__ = [
    'delete_project',
]
