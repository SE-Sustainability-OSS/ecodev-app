"""
File containing the module access selection component for the add user modal in the page rights.
"""
import dash_mantine_components as dmc
from ecodev_front import INDEX
from ecodev_front import LABEL
from ecodev_front import label_text
from ecodev_front import Module
from ecodev_front import MULTI_SELECT
from ecodev_front import section_title
from ecodev_front import subtext
from ecodev_front import TYPE
from ecodev_front import VALUE

from app.constants import MODULE


def module_access_field(modules: list[Module]) -> dmc.Stack:
    """
    Renders the module access section of the 'add user modal'.
    """
    data = [{VALUE: module.name, LABEL: module.name.capitalize()} for module in modules]
    return dmc.Stack([
        section_title('Module access'),
        dmc.Stack([
            label_text('Which module should the user be granted access to ?'),
            subtext('Internal users will be granted access to all modules by default')
        ], gap=0),
        dmc.MultiSelect(
            data=data,
            value=[m[VALUE] for m in data],
            clearable=True,
            id={TYPE: MULTI_SELECT, INDEX: MODULE}),
    ], gap=3, w='80%')
