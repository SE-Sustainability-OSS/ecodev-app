"""
Module implementing an example enum
"""
from enum import Enum
from enum import unique


@unique
class ProductType(str, Enum):
    """
    Example enum
    """
    TECHNOLOGY = 'Technology'
    FOOD = 'Food'
    HEALTH = 'Health'
