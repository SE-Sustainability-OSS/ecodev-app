"""
Module implementing a file upload page
"""
from base64 import b64decode

import dash_mantine_components as dmc
import pandas as pd
from dash import callback
from dash import html
from dash import Input
from dash import no_update
from dash import Output
from ecodev_core import logger_get
from ecodev_front import background_card
from ecodev_front import card_title
from ecodev_front import upload_box

from app.pages.file_upload_page import UPLOAD_BOX_ID
from app.pages.file_upload_page import UPLOAD_OUTPUT_ID

log = logger_get(__name__)
UPLOAD = upload_box(id=UPLOAD_BOX_ID, label='Upload a file (.xlsx/.csv)', multiple=False)
OUTPUT_UPLOAD = html.Div(id=UPLOAD_OUTPUT_ID)
UPLOADERS = background_card(
    [dmc.Stack(
        [
            dmc.Group([card_title('Example file upload'), dmc.Space(w=55),],
                      style={'justify-content': 'space-between'},),
            dmc.Space(h=10), UPLOAD, OUTPUT_UPLOAD
        ]
    )]
)


@callback(Output(UPLOAD_OUTPUT_ID, 'children'),
          Input(UPLOAD_BOX_ID, 'contents'))
def read_file_and_compute(file: str) -> dmc.Text:
    """
    Parse & compute the uploaded excel file.
    """
    if not file:
        return no_update
    try:
        content_string = file.split(',')[1]
        df = pd.read_excel(b64decode(content_string))
        return dmc.Text(f'uploaded data is {len(df)} long (sheet 1)')
    except Exception as e:
        return dmc.Text(f'error {str(e)} has happened')
