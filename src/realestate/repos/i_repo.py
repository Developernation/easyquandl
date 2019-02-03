from interface import Interface

import pandas as pd


class IRepo(Interface):

    @property
    def db_path(self):
        pass

    @staticmethod
    def save(data: pd.DataFrame, path: str) -> None:
        pass

    # TODO CRUD operations
