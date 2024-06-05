"""
Module listing all public method from the db_model modules

Note: Add new tables to the database upon app initialisation by adding them here.
"""
from ecodev_core import AppActivity
from ecodev_core import AppRight
from ecodev_core import AppUser

from app.db_model.product import Product

__all__ = ['AppUser', 'AppRight', 'AppActivity', 'Product']
