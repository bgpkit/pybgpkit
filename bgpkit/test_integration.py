import json
import unittest

import bgpkit


class TestIntegration(unittest.TestCase):

    def test_parser(self):
        parser = bgpkit.Parser(url="https://spaces.bgpkit.org/parser/update-example",
                               filters={"peer_ips": "185.1.8.65, 2001:7f8:73:0:3:fa4:0:1"})
        elems = parser.parse_all()
        assert len(elems) == 4227

    def test_broker(self):
        broker = bgpkit.Broker()
        items = broker.query(ts_start="1643760000", ts_end="2022-02-02T00:20:00")
        for item in items:
            print(json.dumps(item.__dict__))
        print(len(items))
        assert len(items) == 290

        # elems = bgpkit.Parser(items[0].url).parse_all()
        # assert len(elems) == 222467

    def test_broker_2(self):
        broker = bgpkit.Broker()
        items = broker.query(ts_start="1643760000", ts_end="2022-02-02T00:20:00", collector_id="rrc00")
        for item in items:
            print(json.dumps(item.__dict__))
        print(len(items))
        assert len(items) == 7

    def test_roas(self):
        roas = bgpkit.Roas()
        data = roas.query(debug=True, asn=3333, date="2018-01-01")
        for entry in data:
            print(entry)
        assert len(data) == 10

        assert len(roas.query()) == 0
