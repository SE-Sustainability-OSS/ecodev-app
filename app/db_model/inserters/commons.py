from functools import partial

from ecodev_core import upsert_data
from ecodev_core import upsert_selector
from ecodev_core.db_upsertion import upsert_updator
from sqlalchemy.inspection import inspect
from sqlmodel import Session
from sqlmodel.main import SQLModelMetaclass

upsert_data


def upsert_dict(db_schema: SQLModelMetaclass, data: dict, session: Session) -> SQLModelMetaclass:
    """
    Upserts the passed data dict into db_schema db, prior to returning it (if successfu).
    """
    selector = partial(upsert_selector, db_schema=db_schema)
    updator = partial(upsert_updator, db_schema=db_schema)

    filtered_data = {k: v for k, v in data.items()
                     if k in [col.key for col in inspect(db_schema).columns]}

    new_object = db_schema(**filtered_data)
    if in_db := session.exec(selector(new_object)).first():
        session.exec(updator(new_object, in_db.id, session))
    else:
        session.add(new_object)
    session.commit()

    return in_db or new_object
