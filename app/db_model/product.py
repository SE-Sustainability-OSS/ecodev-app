"""
Module implementing an example sql table/python class (alchemy handled by sql...model :))
"""
from datetime import datetime

from sqlmodel import Field
from sqlmodel import SQLModel

from app.domain_model import ProductType


class ProductBase(SQLModel):  # type: ignore
    """
    Example base class. See
    https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/
    for good practice examples.
    """

    id: int | None = Field(default=None, primary_key=True)
    type: ProductType
    name: str
    value: float


class Product(ProductBase, table=True):  # type: ignore
    """
    Example sql table/python class
    """
    __tablename__ = 'product'
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
