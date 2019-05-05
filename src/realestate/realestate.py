import pandas as pd
from typing import List
from pathlib import Path

import quandl
import json

from src.realestate.model.code_combinations import CodeCombinations

class RealEstate:
    # -------------REMEMBER TO ADD YOUR DEVELOPER KEY BELOW---------------------
    # **************************************************************************
    ###########################################################################
    quandl.ApiConfig.api_key = ''
    ###########################################################################
    # **************************************************************************
    # --------------------------------------------------------------------------
    _valid_state_filename: str = 'valid_state_codes.json'
    _invalid_state_filename: str = 'invalid_state_codes.json'

    def __init__(self, data_path: str = './data', force_update: bool = False):
        valid_state_filepath = Path(f"{data_path}/{RealEstate._valid_state_filename}")
        invalid_state_filepath = Path(f"{data_path}/{RealEstate._invalid_state_filename}")

        state_codes: pd.Series = CodeCombinations(data_path=data_path, force_update=force_update).states

        if not force_update and invalid_state_filepath.is_file():
            with open(invalid_state_filepath, 'r') as isfp:
                state_codes = pd.Series(tuple(set(state_codes) - set(json.load(isfp))))
        self.results = []
        self.invalid_state_codes = []
        self.valid_state_codes = []
        for s in state_codes[:10]:
            try:
                result = quandl.get(f'ZILLOW/{s}')
                self.results.append(result)
                self.valid_state_codes.append(s)
            except quandl.errors.quandl_error.NotFoundError:
                self.invalid_state_codes.append(s)

        with open(valid_state_filepath, 'w') as valid_state_file:
            json.dump(self.valid_state_codes, valid_state_file)

        with open(invalid_state_filepath, 'w') as invalid_state_file:
            json.dump(self.invalid_state_codes, invalid_state_file)

r = RealEstate()
print(r.results)
for re in r.results:
    print(re)
print(r.valid_state_codes)
print(r.invalid_state_codes)