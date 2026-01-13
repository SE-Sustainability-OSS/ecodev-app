import dash_mantine_components as dmc
from ecodev_front import INDEX
from ecodev_front import TYPE

from app.domain_model.color_utils import get_color
from app.domain_model.colors import CLAY
from app.domain_model.colors import EARTH
from app.domain_model.colors import GRAY
from app.domain_model.colors import PLANT
from app.domain_model.colors import SAND
from app.domain_model.colors import SEA
from app.pages.module_style_guide.page_colors import COLOR_PALETTE_HEX_BUTTON


def color_palette(name: str, colors: list[str]) -> dmc.Stack:
    """
    Renders the color style guide section
    """
    return dmc.Stack([
        dmc.Title(name, c=colors[6], tt='uppercase', fw=900, fz=16, ta='left'),
        dmc.Group([
            color_box(colors[0], f'{name}.0'),
            color_box(colors[1], f'{name}.1'),
            color_box(colors[2], f'{name}.2'),
            color_box(colors[3], f'{name}.3'),
            color_box(colors[4], f'{name}.4'),
            color_box(colors[5], f'{name}.5'),
            color_box(colors[6], f'{name}.6'),
            color_box(colors[7], f'{name}.7'),
            color_box(colors[8], f'{name}.8'),
            color_box(colors[9], f'{name}.9'),
            color_box(colors[10], f'{name}.10'),
        ])
    ], mb=20, ta='center')


def color_box(color: str, name: str) -> dmc.Stack:
    """
    Renders a colored box, with the color name and hex value,
    to be presented in a style guide.
    """
    return dmc.Stack([
        dmc.Text(name, c='dimmed', fz=12, tt='lowercase', fw=800),
        dmc.Button(id={TYPE: COLOR_PALETTE_HEX_BUTTON, INDEX: get_color(color)},
                   w=80, h=80,
                   style={'border-radius': '10px',
                          'border': '1px solid #dcdcdc',
                          'background-color': get_color(color)}),
        dmc.Code(get_color(color), c='dimmed', fz=12, fs='italic', tt='uppercase')
    ], gap=0, justify='center', align='center')


PRIMARY_COLORS = dmc.Stack([
    dmc.Title('Main', c='gray', tt='uppercase', fw=900, fz=16),
    dmc.Group([
        color_box('blue', 'blue'),
        color_box('green', 'green'),
        color_box('red', 'red'),
        color_box('yellow', 'yellow'),
        color_box('brown', 'brown'),
    ])
], mb=20, ta='center')


GRAY_PALETTE = color_palette(name='gray', colors=GRAY)
SEA_PALETTE = color_palette(name='blue', colors=SEA)
CLAY_PALETTE = color_palette(name='red', colors=CLAY)
PLANT_PALETTE = color_palette(name='green', colors=PLANT)
EARTH_PALETTE = color_palette(name='brown', colors=EARTH)
SAND_PALETTE = color_palette(name='yellow', colors=SAND)
