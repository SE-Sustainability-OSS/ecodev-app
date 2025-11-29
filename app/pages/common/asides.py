from dash import callback
from dash import ctx
from dash import Input
from dash import no_update
from dash import Output
from ecodev_core import logger_get
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

from app.pages.modules import MODULES

log = logger_get(__name__)


@callback(Output(APPSHELL, ASIDE),
          Output(ASIDE, CHILDREN),
          Output(CLOSE_ASIDE_BTN_ID, STYLE),
          Output(OPEN_ASIDE_BTN_ID, STYLE),
          Input(CLOSE_ASIDE_BTN_ID, N_CLICKS),
          Input(OPEN_ASIDE_BTN_ID, N_CLICKS),
          Input(URL, PATHNAME),
          Input(TOKEN, DATA))
def show_asides(close_btn: int, open_btn: int, pathname: str, token: dict):
    """
    Callback displaying the main page navbar and aside (if any)
    """
    width_aside = {'width': '17%'}
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
                page_aside = module.pages[page_index].aside
                return (width_aside, page_aside(), SHOW, HIDE) if page_aside else no_aside

    return no_aside
