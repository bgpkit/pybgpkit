"""Unit tests for AsnLookup, using recorded v3 API response shapes."""

import json
import unittest
from unittest import mock

from bgpkit import BGPKITApiError, AsnInfo, AsnLookup


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload) if payload is not None else ""

    def json(self):
        if self._payload is None:
            raise ValueError("body is not JSON")
        return self._payload


def mock_get(response):
    return mock.patch("bgpkit._utils.requests.get", return_value=response)


ASN_PAYLOAD = {
    "count": 1,
    "data": [
        {
            "as2org": {
                "country": "US",
                "name": "GOOGLE",
                "org_id": "GOGL-ARIN",
                "org_name": "Google LLC",
            },
            "asn": 15169,
            "country": "US",
            "country_name": "United States",
            "hegemony": {"asn": 15169, "ipv4": 0.0079, "ipv6": 0.0027},
            "name": "GOOGLE - Google LLC",
            "peeringdb": {"asn": 15169, "name": "Google LLC", "irr_as_set": "RADB::AS-GOOGLE"},
            "population": {"percent_country": 0, "percent_global": 0, "user_count": 82},
        }
    ],
    "page": 0,
    "page_size": 1,
    "pagination": {
        "page": 0,
        "page_size": 1,
        "total_pages": 1,
        "total_count": 1,
        "has_next": False,
        "has_prev": False,
    },
    "updatedAt": "2026-10-07T12:00:00",
}


class TestAsnLookup(unittest.TestCase):
    def test_parses_nested_asn_item(self):
        with mock_get(FakeResponse(ASN_PAYLOAD)):
            result = AsnLookup().query(asn="15169")
        self.assertEqual(result.count, 1)
        info = result.data[0]
        self.assertIsInstance(info, AsnInfo)
        self.assertEqual(info.asn, 15169)
        self.assertEqual(info.name, "GOOGLE - Google LLC")
        self.assertEqual(info.country_name, "United States")
        self.assertEqual(info.org_name, "Google LLC")
        self.assertEqual(info.org_id, "GOGL-ARIN")
        self.assertEqual(info.hegemony, {"asn": 15169, "ipv4": 0.0079, "ipv6": 0.0027})
        self.assertEqual(result.updated_at, "2026-10-07T12:00:00")
        self.assertIsNotNone(result.pagination)
        self.assertEqual(result.pagination.total_count, 1)
        self.assertFalse(result.pagination.has_next)

    def test_raises_on_http_error(self):
        with mock_get(FakeResponse({"error": "boom"}, status_code=500)):
            with self.assertRaises(BGPKITApiError) as context:
                AsnLookup().query(asn="15169")
        self.assertIn("HTTP 500", str(context.exception))


if __name__ == "__main__":
    unittest.main()
