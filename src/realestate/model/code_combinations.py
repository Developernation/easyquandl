import pandas as pd

from itertools import product
from pathlib import Path
from typing import List

from src.realestate.model.indicator_codes import IndicatorCodes
from src.realestate.model.location_codes import LocationCodes


class CodeCombinations:

    def __init__(self, data_path: str = '.', data_name: str = 'code_combinations.json', force_update: bool = False):
        self._data_path = Path(data_path)
        self._file_path = self._data_path.joinpath(data_name)
        self._series: pd.Series = pd.Series()
        if not force_update and self._file_path.is_file():
            print('Loading code combinations...', end='')
            self._series = pd.read_json(self._file_path, orient='split', typ='series')
            print('done\nLoading state combinations...', end='')
            self._states = self._series[self._series.str.startswith('S', na=False)]
            print('done\nLoading city combinations...', end='')
            self._cities = self._series[(self._series.str.startswith('C', na=False)) &
                                        (~self._series.str.startswith('CO', na=False))]
            print('done\nLoading county combinations...', end='')
            self._counties = self._series[self._series.str.startswith('CO', na=False)]
            print('done\nLoading metro combinations...', end='')
            self._metros = self._series[self._series.str.startswith('M', na=False)]
            print('done\nLoading neighborhood combinations...', end='')
            self._neighborhoods = self._series[self._series.str.startswith('N', na=False)]
            print('done\nLoading zipcode combinations...', end='')
            self._zipcodes = self._series[self._series.str.startswith('Z', na=False)]
            print('done')
        if self._series.empty:
            location_codes: LocationCodes = LocationCodes(data_path=self._data_path, force_update=force_update)
            indicator_codes: pd.Series = IndicatorCodes(data_path=self._data_path, force_update=force_update).df['indicator_code']

            self._states: pd.Series = CodeCombinations.get_combination_code(location_codes.states['location_code'],
                                                                                  indicator_codes)
            self._counties: pd.Series = CodeCombinations.get_combination_code(
                location_codes.counties['location_code'],
                indicator_codes)
            self._metros: pd.Series = CodeCombinations.get_combination_code(location_codes.metros['location_code'],
                                                                                  indicator_codes)
            self._cities: pd.Series = CodeCombinations.get_combination_code(location_codes.cities['location_code'],
                                                                                  indicator_codes)
            self._neighborhoods: pd.Series = CodeCombinations.get_combination_code(
                location_codes.neighborhoods['location_code'],
                indicator_codes)
            self._zipcodes: pd.Series= CodeCombinations.get_combination_code(
                location_codes.zipcodes['location_code'],
                indicator_codes)
            sub_dfs: List[pd.Series] = [self._states, self._counties, self._metros, self._cities, self._neighborhoods,
                                           self._zipcodes]

            self._series = pd.concat(sub_dfs, ignore_index=True, sort=False)
            self._series.to_json(path_or_buf=self._file_path, orient='split', index=False)

    @property
    def series(self) -> pd.Series:
        return self._series.copy()

    @property
    def states(self) -> pd.Series:
        return self._states.copy()

    @property
    def counties(self) -> pd.Series:
        return self._counties.copy()

    @property
    def metros(self) -> pd.Series:
        return self._metros.copy()

    @property
    def cities(self) -> pd.Series:
        return self._cities.copy()

    @property
    def neighborhoods(self) -> pd.Series:
        return self._neighborhoods.copy()

    @property
    def zipcodes(self) -> pd.Series:
        return self._zipcodes.copy()

    @staticmethod
    def get_combination_code(location_codes: pd.Series, indicator_codes: pd.Series) -> pd.Series:
        df = pd.DataFrame([e for e in product(location_codes, indicator_codes)],
                          columns=['location_code', 'indicator_code'])
        df['combined_code'] = df['location_code'].str.cat(df['indicator_code'], sep='_')
        return df['combined_code']

