from dataclasses import dataclass
from typing import List, Optional

from ._utils import DEFAULT_TIMEOUT, from_item, request_json


@dataclass
class CommunityEntry:
    asn: int
    value: str
    description: str
    as_name: str = ""
    country: str = ""
    source: str = ""
    range: Optional[str] = None


@dataclass
class CommunitySource:
    id: str
    name: str
    url: str = ""
    last_updated: Optional[str] = None
    stats: Optional[dict] = None


class CommunityLookup:
    """BGPKIT community lookup (v3/communities)."""

    def __init__(
        self,
        api_url: str = "https://api.bgpkit.com/v3/communities",
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.base_url = api_url.rstrip("/")
        self.timeout = timeout

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
        """Query BGP communities.

        The API returns one entry per ASN with a nested list of communities;
        this returns one CommunityEntry per community.
        """
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

        response = request_json(self.base_url, params=params, timeout=self.timeout)

        entries = []
        for item in response.get("data", []):
            for community in item.get("communities", []) or []:
                entries.append(
                    CommunityEntry(
                        asn=item.get("asn"),
                        value=community.get("community", ""),
                        description=community.get("description") or "",
                        as_name=item.get("name", ""),
                        country=item.get("country", ""),
                        source=community.get("source", ""),
                        range=community.get("range"),
                    )
                )
        return entries

    def sources(self) -> List[CommunitySource]:
        """List the community data sources."""
        response = request_json(f"{self.base_url}/sources", timeout=self.timeout)
        if isinstance(response, list):
            return [from_item(CommunitySource, item) for item in response]
        return [from_item(CommunitySource, item) for item in response.get("sources", [])]
