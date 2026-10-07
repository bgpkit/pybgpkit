from dataclasses import dataclass
from typing import List, Optional

from ._utils import DEFAULT_TIMEOUT, from_item, request_json

DEFAULT_API_URL = "https://api.bgpkit.com/v3/roas"


@dataclass
class RoasItem:
    prefix: str
    asn: int
    max_len: Optional[int] = None
    tal: Optional[str] = None
    current: bool = False
    date_ranges: Optional[List[List[str]]] = None


class Roas:
    """BGPKIT ROAS lookup (v3/roas).

    Queries the ROAS (Route Origin Authorization) database for historical and
    current RPKI data. The base URL can be overridden per instance with
    ``api_url``.
    """

    def __init__(
        self,
        api_url: str = DEFAULT_API_URL,
        page_size: int = 100,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.base_url = api_url.rstrip("/")
        self.page_size = int(page_size)
        self.timeout = timeout

    def query(
        self,
        asn: int = None,
        prefix: str = None,
        date: str = None,
        current: bool = None,
        page: int = 0,
        page_size: int = None,
    ) -> List[RoasItem]:
        """Query the ROAS database, fetching every page from ``page`` onward.

        Args:
            asn: AS number to filter by.
            prefix: IP prefix to filter by.
            date: Date string (YYYY-MM-DD) for historical lookup.
            current: If True, return only currently valid ROAs.
            page: Page number to start from (0-indexed).
            page_size: Results per page (defaults to the instance page size).

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

        size = int(page_size) if page_size is not None else self.page_size
        items: List[RoasItem] = []
        while True:
            page_params = dict(params)
            page_params["page"] = page
            page_params["page_size"] = size
            response = request_json(f"{self.base_url}/search", params=page_params, timeout=self.timeout)

            data = response.get("data", [])
            items.extend(from_item(RoasItem, item) for item in data)

            total = response.get("total")
            if not data or (total is not None and len(items) >= int(total)):
                break
            page += 1

        return items
