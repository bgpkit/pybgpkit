import json
import unittest

import bgpkit


class TestIntegration(unittest.TestCase):

    def test_parser(self):
        parser = bgpkit.Parser(url="https://spaces.bgpkit.org/parser/update-example",
                               filters={"peer_ips": "185.1.8.65, 2001:7f8:73:0:3:fa4:0:1"})
        elems = parser.parse_all()
        self.assertGreater(len(elems), 0)

    def test_route_parser(self):
        parser = bgpkit.RouteParser(url="https://spaces.bgpkit.org/parser/update-example")
        count = parser.count()
        self.assertGreater(count, 0)

    def test_filter(self):
        f = bgpkit.Filter.peer_ip("185.1.8.65")
        self.assertIn("Filter", repr(f))

    def test_broker(self):
        broker = bgpkit.Broker()
        items = broker.query(ts_start="1643760000", ts_end="2022-02-02T00:20:00")
        self.assertGreater(len(items), 0)

        items = broker.query(ts_start="1643760000", ts_end="2022-02-02T00:20:00", collector_id="rrc00")
        self.assertGreater(len(items), 0)

        items = broker.query(ts_start="2022-02-02T00:00:00-00:00", ts_end="2022-02-02T00:20:00.123000+00:00",
                             collector_id="rrc00")
        self.assertGreater(len(items), 0)

    def test_broker_no_verify(self):
        broker = bgpkit.Broker(verify=False)
        items = broker.query(ts_start="1643760000", ts_end="2022-02-02T00:20:00", collector_id="rrc00")
        self.assertGreater(len(items), 0)

    def test_roas(self):
        roas = bgpkit.Roas()
        data = roas.query(asn=3333, date="2018-01-01")
        self.assertGreater(len(data), 0)
