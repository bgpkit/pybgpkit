from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class AsnDetail:
    asn: int
    name: str
    country: str
    org_name: str = ""
    org_id: str = ""


@dataclass
class IpInfo:
    ip: str
    country: str
    asn: Optional[dict] = None

    @property
    def as_number(self) -> Optional[int]:
        if self.asn:
            return self.asn.get("asn")
        return None

    @property
    def as_name(self) -> Optional[str]:
        if self.asn:
            return self.asn.get("name")
        return None


class IpLookup:
    """BGPKIT IP address lookup (v3/utils/ip)."""

    def __init__(self, api_url: str = "https://api.bgpkit.com/v3/utils"):
        self.base_url = api_url.rstrip("/")

    def query(self, ip: str = None, simple: bool = False) -> IpInfo:
        params = {}
        if ip:
            params["ip"] = ip
        if simple:
            params["simple"] = "true"

        res = requests.get(f"{self.base_url}/ip", params=params).json()
        return IpInfo(**res)
