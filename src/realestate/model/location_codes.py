from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd
import requests


class LocationCodes:

    _code_urls = [{"location_type": "S",
                   "url": "https://s3.amazonaws.com/quandl-production-static/zillow/areas_state.txt"},
                  {"location_type": "CO",
                  "url": "https://s3.amazonaws.com/quandl-production-static/zillow/areas_county.txt"},
                  {"location_type": "M",
                   "url": "https://s3.amazonaws.com/quandl-production-static/zillow/areas_metro.txt"},
                  {"location_type": "C",
                   "url": "https://s3.amazonaws.com/quandl-production-static/zillow/areas_city.txt"},
                  {"location_type": "N",
                  "url": "https://s3.amazonaws.com/quandl-production-static/zillow/areas_neighborhood.txt"},
                  ]

    def __init__(self, data_path: str = '.', data_name: str = 'location_codes.json', force_update: bool = False) -> None:
        self._data_path = Path(data_path).joinpath(data_name)
        self._df = pd.DataFrame()
        if not force_update and self._data_path.is_file():
            self._df = pd.read_json(self._data_path, orient='split')

        if self._df.empty:
            codes_df: pd.DataFrame = LocationCodes._fetch_codes_df(LocationCodes._code_urls)
            zipcode_df: pd.DataFrame = pd.DataFrame({"location_type": "Z",
                                                     "number": range(100000)})
            zipcode_df['location_code'] = zipcode_df['number'].apply(lambda n: f"Z{n:05}")
            zipcode_df = zipcode_df.drop(labels='number', axis='columns')

            self._df: pd.DataFrame = pd.concat([zipcode_df, codes_df],
                                               ignore_index=True, sort=False)
            self._df = self._df.drop(labels='location_number', axis='columns')
            self._df.to_json(path_or_buf=self._data_path, orient='split', index=False)
            del codes_df
            del zipcode_df

    @property
    def df(self) -> pd.DataFrame:
        return self._df.copy()

    @property
    def states(self) -> pd.DataFrame:
        return self._df[self._df["location_type"] == 'S']

    @property
    def metros(self) -> pd.DataFrame:
        return self._df[self._df["location_type"] == 'M']

    @property
    def counties(self) -> pd.DataFrame:
        return self._df[self._df["location_type"] == 'CO']

    @property
    def cities(self) -> pd.DataFrame:
        return self._df[self._df["location_type"] == 'C']

    @property
    def neighborhoods(self) -> pd.DataFrame:
        return self._df[self._df["location_type"] == 'N']

    @property
    def zipcodes(self) -> pd.DataFrame:
        return self._df[self._df["location_type"] == 'Z']

    @staticmethod
    def _fetch_codes_df(code_urls: List[Dict[str, str]]) -> pd.DataFrame:
        urls = [e['url'] for e in code_urls]
        location_types = [e['location_type'] for e in code_urls]

        with ThreadPoolExecutor(max_workers=5) as pool:
            location_type_pages: Iterable[Dict[str, str]] = pool.map(LocationCodes._fetch_page, location_types, urls)

        dfs: Iterable[pd.DataFrame] = [LocationCodes._parse(a['page'], a['location_type']) for a in location_type_pages]

        return pd.concat(dfs, ignore_index=True)

    @staticmethod
    def _fetch_page(location_type: str, url: str) -> Dict[str, str]:
        page = requests.get(url).text
        return {'location_type': location_type, 'page': page}

    @staticmethod
    def _parse(page: str, location_type: str) -> pd.DataFrame:
        df: pd.DataFrame = pd.Series(page.split('\n')[1:]  # skip header column
                                     ).str.split('|', expand=True)  # expand into separate columns (DataFrame)
        df = df.dropna()
        df.columns = ('location_name', 'location_code')

        df['location_type'] = location_type
        df['location_number'] = pd.to_numeric(df['location_code'], downcast='integer')
        df['location_code'] = df['location_type'].str.cat(df['location_code'])  # prefix location_type to code

        return df
