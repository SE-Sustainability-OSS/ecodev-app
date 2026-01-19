"""
File containing all color utils methods
"""
from app.domain_model.colors import CLAY
from app.domain_model.colors import COLOR_SCALE_MAPPING
from app.domain_model.colors import EARTH
from app.domain_model.colors import PLANT
from app.domain_model.colors import SAND
from app.domain_model.colors import SEA


def get_color(color: str) -> str:
    """
    Takes in a registered dash-mantine theme color, and returns the appropriate variable.
    This is especially useful to pass dash-mantine theme colors to non dash-mantine components
    (e.g. Plotly or Dash Iconify).

    NB: You can add a .x at the end, where x is an int to get the corresponding scale hue.
    """
    if color.startswith('#'):
        return color
    if color[-1].isnumeric():
        return COLOR_SCALE_MAPPING[color[:-2]][int(color[-1])]
    return COLOR_SCALE_MAPPING[color][7]


def color_way() -> list[str]:
    """
    Renders the default colorway (list of colors) to be used in our graphs
    """
    return [color[hue] for hue in [5, 7, 3, 8, 1, 10, 0]
            for color in [SEA, PLANT, CLAY, SAND, EARTH]]


def color_scale(color: str | None = None, reversed: bool = False) -> list[list[float | str]]:
    """
    Renders the default color scale for a specific color, or for all colors, ensuring enough
    contrast between the color steps.
    """
    if not color or COLOR_SCALE_MAPPING.get(color):
        color = 'blue'

    cs = ((COLOR_SCALE_MAPPING.get(color))[::-1] if reversed
          else COLOR_SCALE_MAPPING.get(color))

    scale = [[idx / (len(cs) - 1), c]
             for idx, c in enumerate(cs)]

    if not reversed:
        scale[0][1] = '#f2f2f2'
    else:
        scale[-1][1] = '#f2f2f2'

    return scale


def diverging_scale() -> list[list[float | str]]:
    """
    Renders a diverging color-scale
    """
    return [[0.0, get_color('red.9')],
            [0.1, get_color('red.7')],
            [0.2, get_color('red.5')],
            [0.3, get_color('red.3')],
            [0.4, get_color('red.1')],
            [0.5, get_color('yellow.1')],
            [0.6, get_color('green.1')],
            [0.7, get_color('green.3')],
            [0.8, get_color('green.5')],
            [0.9, get_color('green.7')],
            [1.0, get_color('green.9')]]


def transform_scale_for_contrast(color_scale: list[str]) -> list[str]:
    """
    Changes the color-scale order to ensure enough contrast between values.
    NOTE: Reduces the scale from 11 values down to 7.
    """
    return [color_scale[5],
            color_scale[3], color_scale[7],
            color_scale[1], color_scale[8],
            color_scale[0], color_scale[10]]
