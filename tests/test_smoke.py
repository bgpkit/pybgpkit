"""Smoke test: verifies parser import and basic iteration works."""

import json

import bgpkit

# Test Parser
parser = bgpkit.Parser(
    url="https://spaces.bgpkit.org/parser/update-example",
    filters={"peer_ips": "185.1.8.65, 2001:7f8:73:0:3:fa4:0:1"},
)
elems = parser.parse_all()
assert len(elems) > 0, "should parse at least one element"
print(f"Parser: {len(elems)} elems")
print(json.dumps(elems[0].to_dict(), indent=2))

# Test RouteParser
route_parser = bgpkit.RouteParser(
    url="https://spaces.bgpkit.org/parser/update-example",
)
count = route_parser.count()
assert count > 0, "should count at least one route"
print(f"RouteParser: {count} routes")

# Test Filter
f = bgpkit.Filter.peer_ip("185.1.8.65")
assert "Filter" in repr(f)
print(f"Filter: {f}")

print("All smoke tests passed")
