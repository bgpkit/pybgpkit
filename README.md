# PyBGPKIT

Python bindings for BGPKIT software. For all software offerings, please check out our GitHub
repository at <https://github.com/bgpkit>.

## SDKs

### BGPKIT Parser

See the [bgpkit-parser-py documentation](https://github.com/bgpkit/bgpkit-parser-py) for the full API.

```python
import bgpkit

# Full element parsing
parser = bgpkit.Parser(url="https://spaces.bgpkit.org/parser/update-example",
                       filters={"peer_ips": "185.1.8.65, 2001:7f8:73:0:3:fa4:0:1"})
for elem in parser:
    print(elem)

# Route-level parsing (faster, fewer fields)
for route in bgpkit.RouteParser(url="https://spaces.bgpkit.org/parser/update-example"):
    print(route.prefix, route.as_path)

# Reusable filter objects
from bgpkit import Filter
f = Filter.peer_ip("185.1.8.65")
parser = bgpkit.Parser.from_filters(url, [f])
```



### BGPKIT Broker

```python
import bgpkit
broker = bgpkit.Broker()

# Search MRT data files
items = broker.query(ts_start="2024-01-01T00:00:00Z", ts_end="2024-01-01T01:00:00Z")
print(len(items))

# Get latest files
latest = broker.latest()

# Query peer information
peers = broker.peers(asn=13335, full_feed=True)

# List collectors
collectors = broker.collectors(project="routeviews", active=True)
```

### BGPKIT IP Lookup

```python
ip_info = bgpkit.IpLookup().query("1.1.1.1")
print(ip_info.country, ip_info.as_number, ip_info.as_name)
```

### BGPKIT ASN Lookup

```python
result = bgpkit.AsnLookup().query(asn="13335", country="US")
for asn in result.data:
    print(asn.asn, asn.name, asn.country)
```

### BGPKIT Community Lookup

```python
entries = bgpkit.CommunityLookup().query(asn="13335", page_size=50)
for entry in entries:
    print(entry.value, entry.description)

sources = bgpkit.CommunityLookup().sources()
```

### BGPKIT ROAS Lookup

### BGPKIT ROAS Lookup

```python
roas = bgpkit.Roas()
data = roas.query(asn=3333, date="2018-01-01")
for entry in data:
    print(entry.prefix, entry.asn, entry.tal)

# Current ROAs only
current = roas.query(prefix="1.1.1.0/24", current=True)
```

## Build and Publish

Push a version tag to build and publish automatically via GitHub Actions:

```
git tag v0.7.0
git push origin v0.7.0
```

Manual release:

```
python -m pip install --upgrade build twine
python -m build
twine upload --skip-existing dist/*
```

PyPI Trusted Publishing is configured for automated releases. See `.github/workflows/release.yml`.

