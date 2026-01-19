"""
File containing our custom ecoact dmc theme, to import into the app_layout
"""
from app.domain_model.colors import COLOR_SCALE_MAPPING

DMC_THEME = {
    'primaryColor': 'blue',
    'colors': COLOR_SCALE_MAPPING,
    'fontFamily': 'Averta',
    'headings': {
        # Properties for all headings
        'fontWeight': '400',
        'fontFamily': 'Stag Sans Book',
        # Properties for individual headings
        'sizes': {
            'h1': {
                'fontWeight': '1000',
                'fontSize': '38px',
                'lineHeight': '1.4',
            },
            'h2': {
                'fontWeight': '900',
                'fontSize': '24px',
                'lineHeight': '1.4',
            },
            'h3': {
                'fontSize': '20px',
                'fontWeight': '800',
                'lineHeight': '1.2',
            },
        },
    },
}
