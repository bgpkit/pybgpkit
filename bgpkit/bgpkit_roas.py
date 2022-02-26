from dataclasses import dataclass
from typing import Optional, List

import requests as requests


def check_type(value: any, ty: type) -> bool:
    try:
        ty(value)
        return True
    except ValueError:
        raise ValueError("invalid option input")


@dataclass
class RoasItem:
    prefix: str
    asn: int
    tal: str
    date_ranges: List[List[str]]


@dataclass
class RoasRes:
    limit: int
    count: int
    data: List[RoasItem]
    next_page_num: Optional[int]
    next_page: Optional[str]
    error: Optional[str]


class Roas:

    def __init__(self, api_url: str = "https://api.roas.bgpkit.com"):
        self.base_url = api_url.strip()

    def query(self,
              prefix: str = None,
              asn: int = None,
              tal: str = None,
              date: str = None,
              max_len: int = None,
              debug: bool = False,
              ) -> [RoasItem]:

        if not (prefix or asn or tal or date or max_len):
            print("ERROR: must specify at least one query parameter: prefix, asn, tal, date, max_len")
            return []

        params = []
        if prefix:
            check_type(prefix, str)
            params.append(f"prefix={prefix}")
        if asn:
            check_type(asn, int)
            params.append(f"asn={asn}")
        if tal:
            check_type(tal, str)
            params.append(f"tal={tal}")
        if date:
            check_type(date, str)
            params.append(f"date={date}")
        if max_len:
            check_type(max_len, int)
            params.append(f"max_len={max_len}")

        api_url = f"{self.base_url}/lookup?" + "&".join(params)
        data_items = []
        if debug:
            print(api_url)
        res = RoasRes(**requests.get(api_url).json())
        while res.data:
            data_items.extend(res.data)
            if res.next_page:
                res = RoasRes(**requests.get(res.next_page).json())
            else:
                break

        return data_items
