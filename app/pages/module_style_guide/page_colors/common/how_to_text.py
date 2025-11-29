"""
File containing the color palette usage instructions.
"""
import dash_mantine_components as dmc
from ecodev_front import section_title
from ecodev_front import text_title


HOW_TO_TEXT = dmc.Group([
    dmc.Stack([
        section_title('How to use the color palette in your apps'),
        dmc.Text("""Each palette color below is embedded into our dash-mantine theme."""),
        dmc.Text("""Therefore when calling a dmc component, you can simply use the color name
                    (e.g. "blue") to get the reference color value, or add another
                    reference number (e.g. "blue.5")"""),
    ], gap=0),
    dmc.Stack([
        text_title('Non dmc components:'),
        dmc.Text("""If calling non dmc components (e.g. DashIconify, DashAgGrid, etc.), you can
                    either simply use the hex value below (click to copy), or use the `get_color`
                    function from app.domain_model to get the color value from the theme."""),
    ], ta='left', gap=0)
], gap=50, grow=True, w='90%', align='flex-end')
