"""
Module and page registry to avoid circular imports when accessing the list of application modules and pages.

This registry is populated during app initialization in page_registry.py, after all modules
and pages have been imported. This allows pages within modules to access the full MODULES and PAGES
lists without creating circular dependencies.
"""
from ecodev_front import Module
from ecodev_front import Page

_MODULE_REGISTRY: list[Module] = []
_PAGE_REGISTRY: list[Page] = []


def add_modules_to_registry(modules: list[Module]) -> None:
    """
    Register the application modules.

    This should be called once during app initialization, after all modules have been imported.

    Args:
        modules: List of Module instances to register
    """
    global _MODULE_REGISTRY
    _MODULE_REGISTRY = modules


def add_pages_to_registry(pages: list[Page]) -> None:
    """
    Register the application pages.

    This should be called once during app initialization, after all pages have been imported.

    Args:
        pages: List of Page instances to register
    """
    global _PAGE_REGISTRY
    _PAGE_REGISTRY = pages


def get_modules(name: str | None = None) -> list[Module] | Module | None:
    """
    Get the registered application modules.
    The function ensures a read-only access to the registry, i.e. prevents users from
    doing the following: _MODULE_REGISTRY.append(some_module).

    Returns:
        List of registered Module instances. Returns empty list if modules haven't been
        registered yet.
    """
    if not name:
        return _MODULE_REGISTRY

    return next((module for module in _MODULE_REGISTRY if module.name == name), None)


def get_pages(name: str | None = None) -> list[Page] | Page | None:
    """
    Get the registered application pages.
    The function ensures a read-only access to the registry, i.e. prevents users from
    doing the following: _PAGE_REGISTRY.append(some_page).

    Returns:
        List of registered Page instances. Returns empty list if pages haven't been
        registered yet.
    """
    if not name:
        return _PAGE_REGISTRY

    return next((page for page in _PAGE_REGISTRY if page.name == name), None)
