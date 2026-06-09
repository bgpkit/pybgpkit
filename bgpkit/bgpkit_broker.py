from dataclasses import dataclass, field
from typing import List, Optional

import requests as requests
import urllib3


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


@dataclass
class PeerItem:
    ip: str
    asn: int
    collector: str
    full_feed: bool = False


@dataclass
class CollectorItem:
    id: str
    name: str
    project: str
    country: str
    active: bool = True
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class LatestResult:
    """Result of the /v3/broker/latest endpoint."""
    items: List[BrokerItem] = field(default_factory=list)


class Broker:
    """BGPKIT Broker v3 API wrapper.

    Provides access to MRT data file search, peer information,
    collector metadata, and latest file discovery.
    """

    def __init__(
        self,
        api_url: str = "https://api.bgpkit.com/v3/broker",
        page_size: int = 100,
        verify: bool = True,
    ):
        self.base_url = api_url.rstrip("/")
        self.page_size = int(page_size)
        self.verify = verify
        if not verify:
            urllib3.disable_warnings()

    def _paginate(self, endpoint: str, params: dict) -> dict:
        """Fetch all pages of a paginated broker endpoint."""
        page = 1
        all_data = []

        while True:
            params["page"] = page
            params["page_size"] = self.page_size
            res = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                verify=self.verify,
            ).json()

            if isinstance(res, dict):
                data = res.get("data", [])
                all_data.extend(data)
                if len(data) < self.page_size:
                    break
            elif isinstance(res, list):
                all_data.extend(res)
                break
            else:
                break

            page += 1

        result = res if isinstance(res, dict) else {"data": all_data}
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
        return [BrokerItem(**item) for item in result.get("data", [])]

    def latest(self) -> List[BrokerItem]:
        """Get latest MRT data files across projects."""
        res = requests.get(
            f"{self.base_url}/latest",
            verify=self.verify,
        ).json()
        if isinstance(res, list):
            return [BrokerItem(**item) for item in res]
        data = res.get("data", [])
        return [BrokerItem(**item) for item in data]

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

        result = self._paginate("peers", params)
        return [PeerItem(**item) for item in result.get("data", [])]

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

        result = self._paginate("collectors", params)
        return [CollectorItem(**item) for item in result.get("data", [])]
