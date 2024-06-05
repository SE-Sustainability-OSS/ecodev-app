"""
Module implementing all sqladmin views
"""
from sqladmin import ModelView

from app.db_model import Product


class ProductAdmin(ModelView, model=Product):  # type: ignore
    """
    Example admin view
    """

    column_list = [Product.id, Product.name, Product.type, Product.value]
    column_searchable_list = [Product.name]
