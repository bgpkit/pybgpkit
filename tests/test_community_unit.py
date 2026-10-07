"""Unit tests for CommunityLookup, using recorded v3 API response shapes."""

import json
import unittest
from unittest import mock

from bgpkit import BGPKITApiError, CommunityEntry, CommunityLookup, CommunitySource


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


COMMUNITIES_PAYLOAD = {
    "total_communities_all": 2,
    "total_communities_on_page": 2,
    "total_asns_on_page": 1,
    "page": 0,
    "page_size": 10,
    "data": [
        {
            "asn": 15169,
            "name": "GOOGLE - Google LLC",
            "country": "US",
            "source": "asn_lookup",
            "communities": [
                {
                    "community": "15169:10010",
                    "source": "nlnog",
                    "description": "GPRS Mobile Broadband",
                    "range": None,
                },
                {
                    "community": "15169:10020",
                    "source": "nlnog",
                    "description": "2.5G/Edge Mobile Broadband",
                    "range": "10.0.0.0/8",
                },
            ],
        }
    ],
}

SOURCES_PAYLOAD = {
    "sources": [
        {
            "id": "nlnog",
            "name": "NLNOG Looking Glass",
            "url": "https://github.com/NLNOG/lg.ring.nlnog.net",
            "last_updated": "2026-10-06T03:00:39.293Z",
            "stats": {"total_asns": 107, "total_communities": 7104, "total_wildcards": 255},
        }
    ]
}


class TestCommunityLookup(unittest.TestCase):
    def test_flattens_communities_per_asn(self):
        with mock_get(FakeResponse(COMMUNITIES_PAYLOAD)):
            entries = CommunityLookup().query(asn="15169")
        self.assertEqual(len(entries), 2)
        entry = entries[0]
        self.assertIsInstance(entry, CommunityEntry)
        self.assertEqual(entry.asn, 15169)
        self.assertEqual(entry.value, "15169:10010")
        self.assertEqual(entry.description, "GPRS Mobile Broadband")
        self.assertEqual(entry.as_name, "GOOGLE - Google LLC")
        self.assertEqual(entry.country, "US")
        self.assertEqual(entry.source, "nlnog")
        self.assertIsNone(entry.range)
        self.assertEqual(entries[1].range, "10.0.0.0/8")

    def test_parses_sources(self):
        with mock_get(FakeResponse(SOURCES_PAYLOAD)):
            sources = CommunityLookup().sources()
        self.assertEqual(len(sources), 1)
        source = sources[0]
        self.assertIsInstance(source, CommunitySource)
        self.assertEqual(source.id, "nlnog")
        self.assertEqual(source.name, "NLNOG Looking Glass")
        self.assertEqual(source.stats["total_communities"], 7104)

    def test_raises_on_http_error(self):
        with mock_get(FakeResponse({"error": "boom"}, status_code=500)):
            with self.assertRaises(BGPKITApiError) as context:
                CommunityLookup().query(asn="15169")
        self.assertIn("HTTP 500", str(context.exception))


if __name__ == "__main__":
    unittest.main()
