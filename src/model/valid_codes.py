#TODO pull webrequests from quandlrealestate.py
#TODO decide whether to just put the data into a db

from concurrent.futures import ThreadPoolExecutor
from typing import List

import pandas as pd


class ValidCodes:

    def __init__(self):
        self.codes: List = ValidCodes.get_codes()
        self.df: pd.DataFrame = pd.concat(self.codes, ignore_index=True)

    @staticmethod
    def get_codes() -> List[str]:
        with ThreadPoolExecutor(max_workers=10) as pool:
            codes = list(*pool.map(ValidCodes._get_codes))
        return codes

    def update(self):
        self.codes = ValidCodes.get_codes()
        self.df = pd.concat(self.codes, ignore_index=True)

    @staticmethod
    def _get_codes(self):
        pass
