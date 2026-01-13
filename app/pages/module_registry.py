"""
Module registry to avoid circular imports when accessing the list of application modules.

This registry is populated during app initialization in page_registry.py, after all modules
have been imported. This allows pages within modules to access the full MODULES list without
creating circular dependencies.
"""
from ecodev_front import Module

_MODULES_REGISTRY: list[Module] = []


def register_modules(modules: list[Module]) -> None:
    """
    Register the application modules.

    This should be called once during app initialization, after all modules have been imported.

    Args:
        modules: List of Module instances to register
    """
    global _MODULES_REGISTRY
    _MODULES_REGISTRY = modules


def get_registered_modules(name: str | None = None) -> list[Module] | Module | None:
    """
    Get the registered application modules.
    The function ensures a read-only access to the registry, i.e. prevents users from
    doing the following: _MODULES_REGISTRY.append(some_module).

    Returns:
        List of registered Module instances. Returns empty list if modules haven't been
        registered yet.
    """
    if not name:
        return _MODULES_REGISTRY

    return next((module for module in _MODULES_REGISTRY if module.name == name), None)
