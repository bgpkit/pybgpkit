from dataclasses import dataclass
from typing import List, Optional

import requests


@dataclass
class Pagination:
    next: Optional[str] = None
    previous: Optional[str] = None


@dataclass
class AsnInfo:
    asn: int
    name: str
    country: str = ""
    org_name: str = ""
    org_id: str = ""
    description: str = ""
    website: str = ""


@dataclass
class AsnLookupResult:
    data: List[AsnInfo]
    count: int
    page: int
    page_size: int
    updated_at: str = ""
    pagination: Optional[Pagination] = None


class AsnLookup:
    """BGPKIT ASN information lookup (v3/utils/asn)."""

    def __init__(self, api_url: str = "https://api.bgpkit.com/v3/utils"):
        self.base_url = api_url.rstrip("/")

    def query(
        self,
        asn: str = None,
        country: str = None,
        search: str = None,
        page: int = 1,
        page_size: int = 100,
    ) -> AsnLookupResult:
        params = {}
        if asn:
            params["asn"] = asn
        if country:
            params["country"] = country
        if search:
            params["search"] = search
        if page:
            params["page"] = page
        if page_size:
            params["page_size"] = min(page_size, 10000)

        res = requests.get(f"{self.base_url}/asn", params=params).json()
        data = [AsnInfo(**item) for item in res.get("data", [])]
        pag = res.get("pagination", {})
        return AsnLookupResult(
            data=data,
            count=res.get("count", 0),
            page=res.get("page", page),
            page_size=res.get("page_size", page_size),
            updated_at=res.get("updatedAt", ""),
            pagination=Pagination(**pag) if pag else None,
        )
