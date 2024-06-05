"""
Module listing all public method from the domain_model modules

You should put here all domain models components not meant to inherit from SQLModel: hence non db dm
"""
from app.domain_model.product_type import ProductType

__all__ = ['ProductType']
