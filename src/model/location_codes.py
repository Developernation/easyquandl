from utils.location.i_location_parser import ILocationParser
from utils.location.location_parser import LocationParser

from concurrent.futures import ThreadPoolExecutor
from tinydb import TinyDB
from typing import Dict, Iterable, List, Tuple, Union

import requests
import ujson


class LocationCodes:

    def __init__(self, location_code_urls_json_path: str = '../data/location_code_urls.json',
                 parser: ILocationParser = LocationParser,
                 out_file: str = '../data/location_codes.json',
                 method: str = 'tinydb') -> None:
        area_type_pages: Iterable[Dict[str, str]] = LocationCodes._fetch_code_pages(location_code_urls_json_path)

        location_code_records: \
            Iterable[Dict[str, Union[str, int]]] = (record for a in area_type_pages
                                                    for record in parser.parse(a['page'], a['area_type']))

        LocationCodes._save_records(location_code_records, out_file, method)
        del area_type_pages
        del location_code_records

    @staticmethod
    def _fetch_code_pages(location_code_urls_json_path: str = '../data/location_code_urls.json') \
            -> Iterable[Dict[str, str]]:
        with open(location_code_urls_json_path, 'r') as in_json:
            location_code_urls: List[Dict[str, Union[str, int]]] = ujson.load(in_json)
        urls: List[str] = []
        area_types: List[str] = []
        for entry in location_code_urls:
            urls.append(entry['url'])
            area_types.append(entry['area_type'])
        with ThreadPoolExecutor(max_workers=5) as pool:
            area_type_pages: Iterable[Dict[str, str]] = pool.map(LocationCodes._fetch_page, area_types, urls)
        return area_type_pages

    @staticmethod
    def _fetch_page(area_type: str, url: str) -> Dict[str, str]:
        page = requests.get(url).text
        return {'area_type': area_type, 'page': page}

    @staticmethod
    def _save_records(records: Iterable[Dict[str, Union[str, int]]],
                      out_file: str = '..data/location_codes.json',
                      method: str = 'tinydb') -> None:
        if method == 'tinydb':
            db = TinyDB(out_file)
            for record in records:
                db.insert(record)
        else:
            raise ValueError(f"Method {method} not yet implemented")

#LocationCodes()
