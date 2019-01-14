from interface import Interface
from typing import Dict, List, Union


class ILocationParser(Interface):

    @staticmethod
    def parse(page: str, area_type: str) -> List[Dict[str, Union[str, int]]]:
        pass
