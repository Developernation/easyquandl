import pandas as pd
from pathlib import Path
import requests


class IndicatorCodes:

    _url = 'https://s3.amazonaws.com/quandl-production-static/zillow/indicators.csv'

    def __init__(self, data_path: str = '.', data_name: str = 'indicator_codes.json', force_update: bool = False) -> None:
        self._data_path = Path(data_path).joinpath(data_name)
        self._df: pd.DataFrame = pd.DataFrame()
        if not force_update and self._data_path.is_file():
            self._df = pd.read_json(self._data_path, orient='split')

        if self._df.empty:
            self._df = IndicatorCodes._get_codes_df(IndicatorCodes._url)
            self._df.to_json(path_or_buf=self._data_path, orient='split', index=False)

    @property
    def df(self) -> pd.DataFrame:
        return self._df.copy()

    @staticmethod
    def _get_codes_df(url: str) -> pd.DataFrame:
        page = requests.get(url).text
        return IndicatorCodes._parse(page)

    @staticmethod
    def _parse(page: str) -> pd.DataFrame:
        df: pd.DataFrame = pd.Series(page.split('\n')[1:]  # skip header column
                                     ).str.split('|', expand=True)  # expand into separate columns (DataFrame)
        df = df.dropna()
        df.columns = ('indicator_description', 'indicator_code')
        return df
