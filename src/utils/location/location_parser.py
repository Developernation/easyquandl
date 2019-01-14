from .i_location_parser import ILocationParser

from interface import implements
from typing import Dict, List, Union
import pandas as pd
import ujson


class LocationParser(implements(ILocationParser)):

    @staticmethod
    def parse(page: str, area_type: str) -> List[Dict[str, Union[str, int]]]:
        df: pd.DataFrame = pd.Series(page.split('\n')[1:]  # skip header column
                                     ).str.split('|', expand=True)  # expand into separate columns (DataFrame)
        df = df.dropna()
        df.columns = ('name', 'code')

        df['area_type'] = area_type
        df['number'] = pd.to_numeric(df['code'], downcast='integer')
        df['code'] = df['area_type'].str.cat(df['code'])  # prefix area_type to code

        return ujson.loads(df.to_json(orient='records'))

