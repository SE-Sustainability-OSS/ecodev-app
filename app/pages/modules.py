"""
File importing and listing all modules across the app.

The list is used throughout the app, to register pages, manage navbar and aside callbacks, etc.

Must be separate from the page_registry and app/pages/common/ as it is imported throughout the app.

NOTE: To manage user-access to the module, you must also add it to the "page rights" under the
project modules (app/pages/module_project/page_rights/page_rights.py), to avoid a circular
reference (as the project module is imported here).
"""


MODULES = []
