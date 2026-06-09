from dataclasses import dataclass
from typing import List, Optional

import requests


@dataclass
class RoasItem:
    prefix: str
    asn: int
    max_len: Optional[int] = None
    tal: Optional[str] = None
    current: bool = False
    date_ranges: Optional[List[List[str]]] = None


class Roas:
    """BGPKIT ROAS lookup (alpha API).

    Queries the ROAS (Route Origination Authorization) database
    for historical and current RPKI data.
    """

    def __init__(self, api_url: str = "https://alpha.api.bgpkit.com"):
        self.base_url = api_url.rstrip("/")

    def query(
        self,
        asn: int = None,
        prefix: str = None,
        date: str = None,
        current: bool = None,
        page: int = 1,
        page_size: int = None,
    ) -> List[RoasItem]:
        """Query ROAS database.

        Args:
            asn: AS number to filter by.
            prefix: IP prefix to filter by.
            date: Date string (YYYY-MM-DD) for historical lookup.
            current: If True, return only currently valid ROAs.
            page: Page number (1-indexed).
            page_size: Results per page. Defaults to 5 (alpha API limitation).

        Returns:
            List of RoasItem matching the query.
        """
        params = {}
        if asn is not None:
            params["asn"] = asn
        if prefix:
            params["prefix"] = prefix
        if date:
            params["date"] = date
        if current is not None:
            params["current"] = str(current).lower()
        params["page"] = str(page)
        params["page_size"] = str(page_size if page_size is not None else 5)

        res = requests.get(f"{self.base_url}/roas", params=params).json()
        if isinstance(res, list):
            return [RoasItem(**item) for item in res]
        return [RoasItem(**item) for item in res.get("data", [])]
