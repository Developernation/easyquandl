from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Iterable, List
import pandas as pd
import requests


class LocationCodes:
    _code_urls = [{"area_type": "S", "url": "https://s3.amazonaws.com/quandl-production-static/zillow/areas_state.txt"},
                  {"area_type": "CO",
                  "url": "https://s3.amazonaws.com/quandl-production-static/zillow/areas_county.txt"},
                  {"area_type": "M", "url": "https://s3.amazonaws.com/quandl-production-static/zillow/areas_metro.txt"},
                  {"area_type": "C", "url": "https://s3.amazonaws.com/quandl-production-static/zillow/areas_city.txt"},
                  {"area_type": "N",
                  "url": "https://s3.amazonaws.com/quandl-production-static/zillow/areas_neighborhood.txt"}]

    def __init__(self) -> None:
        codes_df: pd.DataFrame = LocationCodes._fetch_codes_df(LocationCodes._code_urls)
        zipcode_df: pd.DataFrame = pd.DataFrame({"area_type": "Z",
                                                 "number": range(100000)})
        zipcode_df['code'] = zipcode_df['number'].apply(lambda n: f"Z{n:05}")

        self._df: pd.DataFrame = pd.concat([zipcode_df, codes_df],
                                           ignore_index=True)

        del codes_df
        del zipcode_df


    @property
    def state(self):
        return self._df[self._df["area_type"] == 'S']

    @property
    def metro(self):
        return self._df[self._df["area_type"] == 'S']

    @property
    def county(self):
        return self._df[self._df["area_type"] == 'CO']

    @property
    def city(self):
        return self._df[self._df["area_type"] == 'C']

    @property
    def neighborhood(self):
        return self._df[self._df["area_type"] == 'N']

    @property
    def zipcode(self):
        return self._df[self._df["area_type"] == 'Z']

    @staticmethod
    def _fetch_codes_df(code_urls: List[Dict[str, str]]) -> pd.DataFrame:
        urls = [e['url'] for e in code_urls]
        area_types = [e['area_type'] for e in code_urls]

        with ThreadPoolExecutor(max_workers=5) as pool:
            area_type_pages: Iterable[Dict[str, str]] = pool.map(LocationCodes._fetch_page, area_types, urls)

        dfs: Iterable[pd.DataFrame] = [LocationCodes._parse(a['page'], a['area_type']) for a in area_type_pages]

        return pd.concat(dfs, ignore_index=True)

    @staticmethod
    def _fetch_page(area_type: str, url: str) -> Dict[str, str]:
        page = requests.get(url).text
        return {'area_type': area_type, 'page': page}

    @staticmethod
    def _parse(page: str, area_type: str) -> pd.DataFrame:
        df: pd.DataFrame = pd.Series(page.split('\n')[1:]  # skip header column
                                     ).str.split('|', expand=True)  # expand into separate columns (DataFrame)
        df = df.dropna()
        df.columns = ('name', 'code')

        df['area_type'] = area_type
        df['number'] = pd.to_numeric(df['code'], downcast='integer')
        df['code'] = df['area_type'].str.cat(df['code'])  # prefix area_type to code

        return df


#l = LocationCodes()
#l._df
#l.city
