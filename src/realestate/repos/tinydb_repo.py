import ujson
import pandas as pd

from functools import partial
from interface import implements
from tinydb import TinyDB

from .i_repo import IRepo


class TinyDBRepo(implements(IRepo)):

    def __init__(self, db_path: str):
        self._db_path = db_path
        self.save = partial(TinyDBRepo.save, path=db_path)  # make the instance save method use the path

    @property
    def db_path(self):
        return self._db_path

    @staticmethod
    def save(df: pd.DataFrame, path: str) -> None:
        records = ujson.loads(df.to_json(orient='records'))
        db = TinyDB(path)
        db.purge_tables()  # clear the db
        db.insert_multiple(records)  # thousands of times faster than individual inserts

    # TODO CRUD operations
