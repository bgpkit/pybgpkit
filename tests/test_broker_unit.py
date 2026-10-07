"""Unit tests for the Broker client, using recorded v3 API response shapes."""

import json
import os
import unittest
from unittest import mock

from bgpkit import Broker, BrokerItem, CollectorItem, PeerItem
from bgpkit.bgpkit_broker import DEFAULT_API_URL, BrokerApiError


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
    return mock.patch("bgpkit.bgpkit_broker.requests.get", side_effect=list(responses))


LATEST_PAYLOAD = {
    "count": 2,
    "data": [
        {
            "ts_start": "2026-10-07T14:00:00",
            "ts_end": "2026-10-07T14:00:00",
            "collector_id": "route-views.amsix",
            "data_type": "rib",
            "url": "http://archive.routeviews.org/route-views.amsix/bgpdata/2026.10/RIBS/rib.20261007.1400.bz2",
            "rough_size": 57344000,
            "exact_size": 0,
            "delay": 533,
        },
        {
            "ts_start": "2026-10-07T13:45:00",
            "ts_end": "2026-10-07T14:00:00",
            "collector_id": "route-views.amsix",
            "data_type": "updates",
            "url": "http://archive.routeviews.org/route-views.amsix/bgpdata/2026.10/UPDATES/updates.20261007.1345.bz2",
            "rough_size": 2185216,
            "exact_size": 0,
            "delay": 533,
        },
    ],
    "meta": {"latest_update_ts": "2026-10-07T14:08:53", "latest_update_duration": 1},
}

PEERS_PAYLOAD = {
    "only_full_feed": False,
    "count": 2,
    "last_updated_at": "2026-10-07T14:00:00Z",
    "data": [
        {
            "date": "2026-10-06",
            "collector": "rrc00",
            "ip": "102.208.105.2",
            "asn": 328840,
            "num_v4_pfxs": 1062923,
            "num_v6_pfxs": 0,
            "num_connected_asns": 1,
        },
        {
            "date": "2026-10-06",
            "collector": "rrc00",
            "ip": "102.217.156.3",
            "asn": 328977,
            "num_v4_pfxs": 21163,
            "num_v6_pfxs": 0,
            "num_connected_asns": 120,
        },
    ],
}

COLLECTORS_PAYLOAD = {
    "count": 2,
    "last_updated_at": "2026-10-07T14:00:00.000Z",
    "data": [
        {
            "name": "route-views2",
            "project": "routeviews",
            "data_url": "http://archive.routeviews.org/bgpdata",
            "activated_on": "2003-01-01T00:00:00.000Z",
            "deactivated_on": None,
            "country": "US",
        },
        {
            "name": "route-views.chile",
            "project": "routeviews",
            "data_url": "http://archive.routeviews.org/route-views.chile/bgpdata",
            "activated_on": "2018-01-31T20:00:00.000Z",
            "deactivated_on": "2026-06-01T21:27:00.000Z",
            "country": "CL",
        },
    ],
}

SEARCH_ITEM_A = {
    "ts_start": "2026-10-05T00:00:00",
    "ts_end": "2026-10-05T00:00:00",
    "collector_id": "rrc00",
    "data_type": "rib",
    "url": "https://data.ris.ripe.net/rrc00/2026.10/bview.20261005.0000.gz",
    "rough_size": 146800640,
    "exact_size": 0,
}
SEARCH_ITEM_B = {
    "ts_start": "2026-10-05T00:00:00",
    "ts_end": "2026-10-05T00:05:00",
    "collector_id": "rrc00",
    "data_type": "updates",
    "url": "https://data.ris.ripe.net/rrc00/2026.10/updates.20261005.0000.gz",
    "rough_size": 835584,
    "exact_size": 0,
}
SEARCH_ITEM_C = {
    "ts_start": "2026-10-05T00:05:00",
    "ts_end": "2026-10-05T00:10:00",
    "collector_id": "rrc00",
    "data_type": "updates",
    "url": "https://data.ris.ripe.net/rrc00/2026.10/updates.20261005.0005.gz",
    "rough_size": 790528,
    "exact_size": 0,
}

SEARCH_PAGE_1 = {
    "total": 3,
    "count": 2,
    "page": 1,
    "page_size": 2,
    "error": None,
    "data": [SEARCH_ITEM_A, SEARCH_ITEM_B],
    "meta": {"latest_update_ts": "2026-10-07T14:08:53", "latest_update_duration": 1},
}
SEARCH_PAGE_2 = {
    "total": 3,
    "count": 1,
    "page": 2,
    "page_size": 2,
    "error": None,
    "data": [SEARCH_ITEM_C],
    "meta": {"latest_update_ts": "2026-10-07T14:08:53", "latest_update_duration": 1},
}
SEARCH_PAGE_WITHOUT_TOTAL = {
    "count": 2,
    "data": [SEARCH_ITEM_A, SEARCH_ITEM_B],
}


class TestBrokerLatest(unittest.TestCase):
    def test_parses_items_with_delay_and_ignores_unknown_fields(self):
        payload = json.loads(json.dumps(LATEST_PAYLOAD))
        payload["data"][0]["future_field"] = True
        with mock_get(FakeResponse(payload)) as get:
            items = Broker().latest()
        self.assertEqual(len(items), 2)
        self.assertIsInstance(items[0], BrokerItem)
        self.assertEqual(items[0].collector_id, "route-views.amsix")
        self.assertEqual(items[0].delay, 533)
        self.assertEqual(get.call_count, 1)


class TestBrokerPeers(unittest.TestCase):
    def test_parses_peer_items(self):
        with mock_get(FakeResponse(PEERS_PAYLOAD)) as get:
            peers = Broker(page_size=10).peers(collector="rrc00")
        self.assertEqual(len(peers), 2)
        self.assertIsInstance(peers[0], PeerItem)
        self.assertEqual(peers[0].asn, 328840)
        self.assertTrue(peers[0].full_feed)
        self.assertFalse(peers[1].full_feed)
        # the peers endpoint returns every match in one response
        self.assertEqual(get.call_count, 1)


class TestBrokerCollectors(unittest.TestCase):
    def test_parses_collector_items(self):
        with mock_get(FakeResponse(COLLECTORS_PAYLOAD)) as get:
            collectors = Broker(page_size=10).collectors(project="routeviews")
        self.assertEqual(len(collectors), 2)
        self.assertIsInstance(collectors[0], CollectorItem)
        self.assertEqual(collectors[0].name, "route-views2")
        self.assertTrue(collectors[0].active)
        self.assertFalse(collectors[1].active)
        self.assertEqual(collectors[1].deactivated_on, "2026-06-01T21:27:00.000Z")
        self.assertEqual(get.call_count, 1)


class TestBrokerQuery(unittest.TestCase):
    def test_paginates_until_total_is_reached(self):
        responses = [FakeResponse(SEARCH_PAGE_1), FakeResponse(SEARCH_PAGE_2)]
        with mock_get(*responses) as get:
            items = Broker(page_size=2).query(collector_id="rrc00")
        self.assertEqual([item.url for item in items], [SEARCH_ITEM_A["url"], SEARCH_ITEM_B["url"], SEARCH_ITEM_C["url"]])
        self.assertEqual(get.call_count, 2)
        self.assertEqual(get.call_args_list[1].kwargs["params"]["page"], 2)

    def test_stops_when_a_page_adds_no_new_items(self):
        responses = [FakeResponse(SEARCH_PAGE_WITHOUT_TOTAL), FakeResponse(SEARCH_PAGE_WITHOUT_TOTAL)]
        with mock_get(*responses) as get:
            items = Broker(page_size=2).query()
        self.assertEqual(len(items), 2)
        self.assertEqual(get.call_count, 2)

    def test_raises_on_http_error(self):
        with mock_get(FakeResponse({"error": "boom"}, status_code=500)):
            with self.assertRaises(BrokerApiError) as context:
                Broker().query(collector_id="rrc00")
        self.assertIn("HTTP 500", str(context.exception))


class TestBrokerConfiguration(unittest.TestCase):
    def test_default_api_url(self):
        environment = {key: value for key, value in os.environ.items() if key != "BGPKIT_BROKER_URL"}
        with mock.patch.dict(os.environ, environment, clear=True):
            self.assertEqual(Broker().base_url, DEFAULT_API_URL)

    def test_environment_variable_overrides_default(self):
        with mock.patch.dict(os.environ, {"BGPKIT_BROKER_URL": "https://broker.example.com/v2/broker/"}):
            self.assertEqual(Broker().base_url, "https://broker.example.com/v2/broker")

    def test_explicit_argument_wins_over_environment(self):
        with mock.patch.dict(os.environ, {"BGPKIT_BROKER_URL": "https://broker.example.com/v2/broker"}):
            self.assertEqual(
                Broker(api_url="https://other.example.com/broker").base_url,
                "https://other.example.com/broker",
            )


if __name__ == "__main__":
    unittest.main()
