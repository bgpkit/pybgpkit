import json
import os
from dataclasses import dataclass
from typing import List, Optional

import urllib3

from ._utils import DEFAULT_TIMEOUT, BGPKITApiError, from_item, request_json

DEFAULT_API_URL = "https://api.bgpkit.com/v3/broker"


def check_type(value: any, ty: type) -> bool:
    try:
        ty(value)
        return True
    except (ValueError, TypeError):
        raise ValueError("invalid option input")


@dataclass
class BrokerItem:
    ts_start: str
    ts_end: str
    collector_id: str
    data_type: str
    url: str
    rough_size: int
    exact_size: int
    delay: Optional[float] = None  # seconds since the latest catalog update; /latest items only


@dataclass
class PeerItem:
    date: str
    collector: str
    ip: str
    asn: int
    num_v4_pfxs: int
    num_v6_pfxs: int
    num_connected_asns: int

    @property
    def full_feed(self) -> bool:
        """True for full-table peers (>700k IPv4 or >100k IPv6 prefixes)."""
        return self.num_v4_pfxs > 700_000 or self.num_v6_pfxs > 100_000


@dataclass
class CollectorItem:
    name: str
    project: str
    data_url: str
    activated_on: str
    deactivated_on: Optional[str]
    country: str

    @property
    def active(self) -> bool:
        return self.deactivated_on is None


class Broker:
    """BGPKIT Broker v3 API wrapper.

    Provides access to MRT data file search, peer information,
    collector metadata, and latest file discovery.

    The API base URL can be overridden per instance with ``api_url`` or for the
    whole process with the ``BGPKIT_BROKER_URL`` environment variable.
    """

    def __init__(
        self,
        api_url: Optional[str] = None,
        page_size: int = 100,
        verify: bool = True,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        if api_url is None:
            api_url = os.environ.get("BGPKIT_BROKER_URL") or DEFAULT_API_URL
        self.base_url = api_url.rstrip("/")
        self.page_size = int(page_size)
        self.verify = verify
        self.timeout = timeout
        if not verify:
            urllib3.disable_warnings()

    def _request(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make a single request and return the parsed JSON body."""
        return request_json(
            f"{self.base_url}/{endpoint}",
            params=params,
            verify=self.verify,
            timeout=self.timeout,
        )

    def _paginate(self, endpoint: str, params: dict) -> dict:
        """Fetch every page of a paginated broker endpoint.

        Stops when the reported total is reached, or when a page adds no new
        items. The latter also terminates endpoints that ignore pagination
        parameters instead of looping on the same full page forever.
        """
        page = 1
        all_data: List[dict] = []
        seen = set()
        result = {}
        while True:
            page_params = dict(params)
            page_params["page"] = page
            page_params["page_size"] = self.page_size

            result = self._request(endpoint, page_params)
            data = result.get("data", [])
            new_items = []
            for item in data:
                key = json.dumps(item, sort_keys=True, default=str)
                if key not in seen:
                    seen.add(key)
                    new_items.append(item)
            all_data.extend(new_items)

            total = result.get("total")
            if not data or not new_items:
                break
            if total is not None and len(all_data) >= int(total):
                break
            page += 1

        result["data"] = all_data
        return result

    def query(
        self,
        ts_start: str = None,
        ts_end: str = None,
        collector_id: str = None,
        project: str = None,
        data_type: str = None,
    ) -> List[BrokerItem]:
        """Search for MRT data files matching the given criteria."""
        params = {}
        if ts_start:
            params["ts_start"] = ts_start
        if ts_end:
            params["ts_end"] = ts_end
        if collector_id:
            params["collector_id"] = collector_id
        if project:
            check_type(project, str)
            params["project"] = project
        if data_type:
            check_type(data_type, str)
            params["data_type"] = data_type

        result = self._paginate("search", params)
        return [from_item(BrokerItem, item) for item in result.get("data", [])]

    def latest(self) -> List[BrokerItem]:
        """Get the latest MRT data file for every collector and data type."""
        result = self._request("latest")
        return [from_item(BrokerItem, item) for item in result.get("data", [])]

    def peers(
        self,
        full_feed: bool = None,
        ip: str = None,
        asn: int = None,
        collector: str = None,
    ) -> List[PeerItem]:
        """Query BGP peer information."""
        params = {}
        if full_feed is not None:
            params["full_feed"] = str(full_feed).lower()
        if ip:
            params["ip"] = ip
        if asn:
            params["asn"] = asn
        if collector:
            params["collector"] = collector

        result = self._request("peers", params)
        return [from_item(PeerItem, item) for item in result.get("data", [])]

    def collectors(
        self,
        project: str = None,
        country: str = None,
        active: bool = None,
    ) -> List[CollectorItem]:
        """Query MRT collector information."""
        params = {}
        if project:
            params["project"] = project
        if country:
            params["country"] = country
        if active is not None:
            params["active"] = str(active).lower()

        result = self._request("collectors", params)
        return [from_item(CollectorItem, item) for item in result.get("data", [])]
