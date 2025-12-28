"""
File containing definition of the style-guide module and its pages.
"""
from ecodev_front import icon_navbar
from ecodev_front import Module

from app.domain_model import AppModule
from app.domain_model.color_utils import get_color
from app.pages.module_style_guide.page_colors.page_colors import PAGE_COLORS
from app.pages.module_style_guide.page_components.page_components import PAGE_COMPONENTS
from app.pages.module_style_guide.page_graphs.page_graphs import PAGE_GRAPHS
from app.pages.module_style_guide.page_typography.page_typography import PAGE_TYPO


MODULE_STYLE_GUIDE = Module(
    file=__name__,
    name=AppModule.STYLE_GUIDE.value,
    description='To provides uniformity in style and formatting within our apps.',
    icon='material-symbols:style',
    pages=[
        PAGE_COLORS,
        PAGE_TYPO,
        PAGE_COMPONENTS,
        PAGE_GRAPHS
    ],
    navbar_layout=icon_navbar,
    main_page_button_kwargs=dict(label_top='Consult',
                                 label_bottom='Style Guide',
                                 color=get_color('red.5'))
)
