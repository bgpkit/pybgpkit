from dataclasses import dataclass
from typing import List, Optional

from ._utils import DEFAULT_TIMEOUT, from_item, request_json


@dataclass
class Pagination:
    page: int = 0
    page_size: int = 0
    total_pages: int = 0
    total_count: int = 0
    has_next: bool = False
    has_prev: bool = False


@dataclass
class AsnInfo:
    asn: int
    name: str
    country: str = ""
    country_name: str = ""
    org_name: str = ""
    org_id: str = ""
    as2org: Optional[dict] = None
    hegemony: Optional[dict] = None
    peeringdb: Optional[dict] = None
    population: Optional[dict] = None


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

    def __init__(
        self,
        api_url: str = "https://api.bgpkit.com/v3/utils",
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.base_url = api_url.rstrip("/")
        self.timeout = timeout

    def query(
        self,
        asn: str = None,
        country: str = None,
        search: str = None,
        page: int = 1,
        page_size: int = 100,
    ) -> AsnLookupResult:
        """Look up ASN information.

        Args:
            asn: AS number, or a comma-separated list of AS numbers.
            country: Filter by ISO country code.
            search: Free-text search over ASN names and organizations.
            page: Page number (1-indexed).
            page_size: Results per page.

        Returns:
            AsnLookupResult with the parsed ASN entries and pagination info.
        """
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

        response = request_json(f"{self.base_url}/asn", params=params, timeout=self.timeout)

        data = []
        for item in response.get("data", []):
            as2org = item.get("as2org") if isinstance(item.get("as2org"), dict) else {}
            data.append(
                AsnInfo(
                    asn=item.get("asn"),
                    name=item.get("name", ""),
                    country=item.get("country", ""),
                    country_name=item.get("country_name", ""),
                    org_name=as2org.get("org_name", ""),
                    org_id=as2org.get("org_id", ""),
                    as2org=as2org or None,
                    hegemony=item.get("hegemony"),
                    peeringdb=item.get("peeringdb"),
                    population=item.get("population"),
                )
            )

        pagination_data = response.get("pagination")
        pagination = (
            from_item(Pagination, pagination_data) if isinstance(pagination_data, dict) else None
        )

        return AsnLookupResult(
            data=data,
            count=response.get("count", 0),
            page=response.get("page", page),
            page_size=response.get("page_size", page_size),
            updated_at=response.get("updatedAt", ""),
            pagination=pagination,
        )
