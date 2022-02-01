# PyBGPKIT

Python bindings for BGPKIT software. For all software offerings, please check out our GitHub
repository at <https://github.com/bgpkit>.

## SDKs

### BGPKIT Parser

Original Rust BGPKIT Parser code available at: <https://github.com/bgpkit/bgpkit-parser> 

Example:
```python
import bgpkit
parser = bgpkit.Parser(url="https://spaces.bgpkit.org/parser/update-example",
                       filters={"peer_ips": "185.1.8.65, 2001:7f8:73:0:3:fa4:0:1"})
elems = parser.parse_all()
assert len(elems) == 4227
```

The `Parser` constructor takes two parameters:
- `url`: the URL or local file path toward an MRT file
- `fitlers`: a dictionary of filters, available filters are:
  - `origin_asn`: origin AS number
  - `prefix`: exact match prefix
    - `prefix_super`: exact prefix and its super prefixes
    - `prefix_sub`: exact prefix and its sub prefixes
    - `prefix_super_sub`: exact prefix and its super and sub prefixes
  - `peer_ip`: peer's IP address
  - `peer_ips`: peers' IP addresses
  - `peer_asn`: peer's ASN
  - `type`: message type (`withdraw` or `announce`)
  - `ts_start`: start unix timestamp
  - `ts_end`: end unix timestamp
  - `as_path`: regular expression for AS path string


Each returning item has the following field:
- `timestamp`: float, unix timestamp
- `elem_type`: str, `A`, announcement; `W`, withdrawn
- `peer_ip`: str, peer IP address
- `peer_asn`: int, peer ASN
- `prefix`: str, the announced/withdrawn IP prefix
- `next_hop`: str or None, next hop IP address
- `as_path`: str or None, AS path str, e.g. `60924 6939 58715 63969 135490`
- `origin_asns`: [int] or None, array of originating ASNs of the prefix
- `origin`: str or None, `IGP`, `EGP`, or `INCOMPLETE`
- `local_pref`: int or None, local preference
- `med`: int or None, multi-exitmultiple exit discriminator
- `communities`: [str] or None, community values, e.g. `['60924:6', '60924:150', '60924:502', '60924:2002', 'ecop:67:0:000000000000']`
- `atomic`: str, `AG` for atomic aggregate, and `NAG` for non-atomic aggregate
- `aggr_ip`: str or None, aggregator IP address
- `aggr_asn`: int or None, aggregator ASN



### BGPKIT Broker

Origianl Rust version BGPKIT Broker code available at: <https://github.com/bgpkit/bgpkit-broker>

Example:
```python
import bgpkit
broker = bgpkit.Broker()
items = broker.query(start_ts=1634693400, end_ts=1634693400)
for item in items:
    print(item)
print(len(items))
assert len(items) == 58
```

Available fields:

- `Broker()`
  - `api_url`: the base URL for the BGPKIT Broker instance. Default: `https://api.broker.bgpkit.com/v1`
  - `page_size`: the number of items per API call (no need to change it). Default: 100.
- `query()`
  - `start_ts`: start timestamp for MRT file, UNIX timestamp format
  - `end_ts`: end timestamp for MRT file, UNIX timestamp format
  - `collector`: collector name, e.g. `rrc00` or `route-views2`
  - `data_type`: `rib` or `update`
  - `order`: order by timestamp, `asc` or `desc`, default

