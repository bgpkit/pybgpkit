"""Unit tests for the shared API helpers."""

import json
import unittest
from dataclasses import dataclass
from unittest import mock

import requests

from bgpkit._utils import BGPKITApiError, from_item, request_json


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload) if payload is not None else ""

    def json(self):
        if self._payload is None:
            raise ValueError("body is not JSON")
        return self._payload


class TestRequestJson(unittest.TestCase):
    def test_returns_parsed_json(self):
        with mock.patch(
            "bgpkit._utils.requests.get", return_value=FakeResponse({"ok": True})
        ) as get:
            result = request_json("https://api.example.com/x", params={"a": 1})
        self.assertEqual(result, {"ok": True})
        self.assertEqual(get.call_args.kwargs["params"], {"a": 1})

    def test_wraps_transport_failures(self):
        with mock.patch(
            "bgpkit._utils.requests.get", side_effect=requests.ConnectionError("boom")
        ):
            with self.assertRaises(BGPKITApiError) as context:
                request_json("https://api.example.com/x")
        self.assertIn("failed", str(context.exception))

    def test_wraps_timeouts(self):
        with mock.patch("bgpkit._utils.requests.get", side_effect=requests.Timeout("too slow")):
            with self.assertRaises(BGPKITApiError):
                request_json("https://api.example.com/x")

    def test_wraps_non_json_bodies(self):
        with mock.patch("bgpkit._utils.requests.get", return_value=FakeResponse(None)):
            with self.assertRaises(BGPKITApiError) as context:
                request_json("https://api.example.com/x")
        self.assertIn("non-JSON", str(context.exception))


class TestFromItem(unittest.TestCase):
    def test_ignores_unknown_fields(self):
        @dataclass
        class Item:
            a: int
            b: str = ""

        self.assertEqual(from_item(Item, {"a": 1, "b": "x", "c": 2}), Item(a=1, b="x"))


if __name__ == "__main__":
    unittest.main()
