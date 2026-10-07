"""Shared helpers for the BGPKIT API clients."""

from dataclasses import fields
from typing import Optional

import requests

DEFAULT_TIMEOUT = 30.0


class BGPKITApiError(RuntimeError):
    """Raised when an API request fails or returns an error response."""


def from_item(cls, item: dict):
    """Build a dataclass from an API item, ignoring unknown fields."""
    names = {field.name for field in fields(cls)}
    return cls(**{key: value for key, value in item.items() if key in names})


def request_json(
    url: str,
    params: Optional[dict] = None,
    verify: bool = True,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    """GET a JSON API endpoint, raising BGPKITApiError on failures."""
    response = requests.get(url, params=params or {}, verify=verify, timeout=timeout)
    if response.status_code >= 400:
        raise BGPKITApiError(
            f"GET {url} failed with HTTP {response.status_code}: {response.text[:200]}"
        )
    try:
        return response.json()
    except ValueError as error:
        raise BGPKITApiError(f"GET {url} returned a non-JSON response") from error
