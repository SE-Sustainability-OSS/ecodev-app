from dash import callback
from dash import ctx
from dash import Input
from dash import no_update
from dash import Output
from dash import State
from ecodev_core import engine
from ecodev_core import safe_get_user
from ecodev_front import APPSHELL
from ecodev_front import ASIDE
from ecodev_front import CHILDREN
from ecodev_front import CLOSE_ASIDE_BTN_ID
from ecodev_front import DATA
from ecodev_front import HIDE
from ecodev_front import N_CLICKS
from ecodev_front import OPEN_ASIDE_BTN_ID
from ecodev_front import PATHNAME
from ecodev_front import SHOW
from ecodev_front import STYLE
from ecodev_front import TOKEN
from ecodev_front import URL
from sqlmodel import Session

from app.constants import PROJECT_ID_STORE
from app.pages.modules import MODULES


@callback(Output(APPSHELL, ASIDE),
          Output(ASIDE, CHILDREN),
          Output(CLOSE_ASIDE_BTN_ID, STYLE),
          Output(OPEN_ASIDE_BTN_ID, STYLE),
          Input(TOKEN, DATA),
          State(PROJECT_ID_STORE, DATA),
          Input(CLOSE_ASIDE_BTN_ID, N_CLICKS),
          Input(OPEN_ASIDE_BTN_ID, N_CLICKS),
          Input(URL, PATHNAME))
def show_asides(token: dict, project_id: int, close_btn: int, open_btn: int, pathname: str):
    """
    Callback displaying the main page navbar and aside (if any).

    NOTE: This callback assumes all aside params are token, project_id and session.
    """
    width_aside = {'width': '275px'}
    width_none = {'width': 0}
    no_aside = (width_none, [], HIDE, HIDE)  # type: ignore[var-annotated]

    if safe_get_user(token):
        for module in MODULES:
            if pathname in [page.url for page in module.pages]:
                if open_btn and ctx.triggered_id == OPEN_ASIDE_BTN_ID:
                    return width_aside, no_update, SHOW, HIDE

                if close_btn and ctx.triggered_id == CLOSE_ASIDE_BTN_ID:
                    return width_none, no_update, HIDE, SHOW

                page_index = [page.url for page in module.pages].index(pathname)
                if not (page_aside := module.pages[page_index].aside):
                    return no_aside

                with Session(engine) as session:
                    return width_aside, page_aside(token, project_id, session), SHOW, HIDE

    return no_aside
