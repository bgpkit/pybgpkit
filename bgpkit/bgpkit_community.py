from dataclasses import dataclass
from typing import List, Optional

import requests


@dataclass
class CommunityEntry:
    asn: int
    value: str
    description: str
    as_name: str = ""
    country: str = ""
    source: str = ""


@dataclass
class CommunitySource:
    id: str
    name: str
    url: str = ""


class CommunityLookup:
    """BGPKIT community lookup (v3/communities)."""

    def __init__(self, api_url: str = "https://api.bgpkit.com/v3/communities"):
        self.base_url = api_url.rstrip("/")

    def query(
        self,
        asn: str = None,
        value: str = None,
        description: str = None,
        as_name: str = None,
        country: str = None,
        page: int = 0,
        page_size: int = 10,
    ) -> List[CommunityEntry]:
        params = {}
        if asn:
            params["asn"] = asn
        if value:
            params["value"] = value
        if description:
            params["description"] = description
        if as_name:
            params["as_name"] = as_name
        if country:
            params["country"] = country
        params["page"] = str(page)
        params["page_size"] = str(min(page_size, 1000))

        res = requests.get(self.base_url, params=params).json()
        if isinstance(res, list):
            return [CommunityEntry(**item) for item in res]
        return [CommunityEntry(**item) for item in res.get("data", [])]

    def sources(self) -> List[CommunitySource]:
        res = requests.get(f"{self.base_url}/sources").json()
        if isinstance(res, list):
            return [CommunitySource(**item) for item in res]
        return [CommunitySource(**item) for item in res.get("data", [])]
