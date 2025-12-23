"""
Module implementing all sqladmin views
"""
from sqladmin import ModelView

from app.db_model.project import Project


class ProjectAdmin(ModelView, model=Project):  # type: ignore
    """
    Example: Project admin view
    """
    column_list = [Project.id, Project.name, Project.description, Project.year]
    column_searchable_list = [Project.name, Project.year]
