"""Unit tests for Roas, using recorded v3 API response shapes."""

import json
import unittest
from unittest import mock

from bgpkit import BGPKITApiError, Roas, RoasItem


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload) if payload is not None else ""

    def json(self):
        if self._payload is None:
            raise ValueError("body is not JSON")
        return self._payload


def mock_get(*responses):
    return mock.patch("bgpkit._utils.requests.get", side_effect=list(responses))


ROAS_ITEM_A = {
    "prefix": "193.0.20.0/23",
    "max_len": 23,
    "asn": 3333,
    "date_ranges": [["2015-03-10", "2016-01-26"]],
    "current": False,
}
ROAS_ITEM_B = {
    "prefix": "193.0.22.0/23",
    "max_len": 23,
    "asn": 3333,
    "date_ranges": [["2015-03-10", "2024-01-01"], ["2024-06-01", "2026-10-07"]],
    "current": True,
}
ROAS_ITEM_C = {
    "prefix": "193.0.24.0/23",
    "max_len": 23,
    "asn": 3333,
    "date_ranges": [["2015-03-10", "2024-01-01"]],
    "current": False,
}

ROAS_PAGE_1 = {
    "total": 3,
    "page": 1,
    "page_size": 2,
    "error": None,
    "data": [ROAS_ITEM_A, ROAS_ITEM_B],
    "meta": {"latest_date": "2026-10-07"},
}
ROAS_PAGE_2 = {
    "total": 3,
    "page": 2,
    "page_size": 2,
    "error": None,
    "data": [ROAS_ITEM_C],
    "meta": {"latest_date": "2026-10-07"},
}


class TestRoas(unittest.TestCase):
    def test_default_api_url_is_v3(self):
        self.assertEqual(Roas().base_url, "https://api.bgpkit.com/v3/roas")

    def test_paginates_until_total_is_reached(self):
        with mock_get(FakeResponse(ROAS_PAGE_1), FakeResponse(ROAS_PAGE_2)) as get:
            items = Roas(page_size=2).query(asn=3333)
        self.assertEqual([item.prefix for item in items], [ROAS_ITEM_A["prefix"], ROAS_ITEM_B["prefix"], ROAS_ITEM_C["prefix"]])
        self.assertIsInstance(items[0], RoasItem)
        self.assertEqual(items[1].current, True)
        self.assertEqual(get.call_count, 2)
        self.assertTrue(get.call_args_list[0].args[0].endswith("/search"))
        # the ROAS endpoint uses a 0-indexed page parameter
        self.assertEqual(get.call_args_list[0].kwargs["params"]["page"], 0)
        self.assertEqual(get.call_args_list[1].kwargs["params"]["page"], 1)

    def test_raises_on_http_error(self):
        with mock_get(FakeResponse({"error": "boom"}, status_code=500)):
            with self.assertRaises(BGPKITApiError) as context:
                Roas().query(asn=3333)
        self.assertIn("HTTP 500", str(context.exception))


if __name__ == "__main__":
    unittest.main()
