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

Original Rust version BGPKIT Broker code available at: <https://github.com/bgpkit/bgpkit-broker>

Example:
```python
import bgpkit
broker = bgpkit.Broker()
items = broker.query(ts_start="1634693400", ts_end="2021-10-20T01:30:00")
for item in items:
    print(item)
print(len(items))
assert len(items) == 58
```

Available fields:

- `Broker()`
  - `api_url`: the base URL for the BGPKIT Broker instance. Default: `https://api.broker.bgpkit.com/v2`
  - `page_size`: the number of items per API call (no need to change it). Default: 100.
- `query()`
  - `ts_start`: start timestamp for MRT file, UNIX timestamp format
  - `ts_end`: end timestamp for MRT file, UNIX timestamp format
  - `collector`: collector name, e.g. `rrc00` or `route-views2`
  - `data_type`: `rib` or `update`
  
### BGPKIT ROAS Lookup

BGPKIT ROAS lookup API provides lookup for historical RPKI ROAS data lookup. The following example shows a query that
asks for all the validated ROA payload for RIPE NCC on the date of `2018-01-01`.

```python
import bgpkit
roas = bgpkit.Roas()
data = roas.query(debug=True, asn=3333, date="2018-01-01")
for entry in data:
    print(entry)
assert len(data) == 10
```

``` 
{'tal': 'ripencc', 'prefix': '193.0.0.0/21', 'asn': 3333, 'max_len': 21, 'date_ranges': [['2015-03-10', '2016-01-26'], ['2016-01-30', '2018-12-27'], ['2019-01-03', '2019-10-21'], ['2019-10-23', '2020-02-23'], ['2020-02-25', '2020-04-05'], ['2020-04-07', '2020-08-02'], ['2020-08-04', '2021-04-21'], ['2021-04-23', '2021-04-24'], ['2021-04-28', '2022-02-26']]}
{'tal': 'ripencc', 'prefix': '193.0.10.0/23', 'asn': 3333, 'max_len': 23, 'date_ranges': [['2015-03-10', '2016-01-26'], ['2016-01-30', '2018-12-27'], ['2019-01-03', '2019-10-21'], ['2019-10-23', '2020-02-23'], ['2020-02-25', '2020-04-05'], ['2020-04-07', '2020-08-02'], ['2020-08-04', '2021-04-21'], ['2021-04-23', '2021-04-24'], ['2021-04-28', '2022-02-26']]}
{'tal': 'ripencc', 'prefix': '193.0.12.0/23', 'asn': 3333, 'max_len': 23, 'date_ranges': [['2015-03-10', '2016-01-26'], ['2016-01-30', '2018-12-27'], ['2019-01-03', '2019-10-21'], ['2019-10-23', '2020-02-23'], ['2020-02-25', '2020-04-05'], ['2020-04-07', '2020-08-02'], ['2020-08-04', '2021-04-21'], ['2021-04-23', '2021-04-24'], ['2021-04-28', '2022-02-26']]}
{'tal': 'ripencc', 'prefix': '193.0.18.0/23', 'asn': 3333, 'max_len': 23, 'date_ranges': [['2015-03-10', '2016-01-26'], ['2016-01-30', '2018-12-27'], ['2019-01-03', '2019-10-21'], ['2019-10-23', '2020-02-23'], ['2020-02-25', '2020-04-05'], ['2020-04-07', '2020-08-02'], ['2020-08-04', '2021-04-21'], ['2021-04-23', '2021-04-24'], ['2021-04-28', '2022-02-26']]}
{'tal': 'ripencc', 'prefix': '193.0.20.0/23', 'asn': 3333, 'max_len': 23, 'date_ranges': [['2015-03-10', '2016-01-26'], ['2016-01-30', '2018-12-27'], ['2019-01-03', '2019-10-21'], ['2019-10-23', '2020-02-23'], ['2020-02-25', '2020-04-05'], ['2020-04-07', '2020-08-02'], ['2020-08-04', '2021-04-21'], ['2021-04-23', '2021-04-24'], ['2021-04-28', '2022-02-26']]}
{'tal': 'ripencc', 'prefix': '193.0.22.0/23', 'asn': 3333, 'max_len': 23, 'date_ranges': [['2015-03-10', '2016-01-26'], ['2016-01-30', '2018-12-27'], ['2019-01-03', '2019-10-21'], ['2019-10-23', '2020-02-23'], ['2020-02-25', '2020-04-05'], ['2020-04-07', '2020-08-02'], ['2020-08-04', '2021-04-21'], ['2021-04-23', '2021-04-24'], ['2021-04-28', '2022-02-26']]}
{'tal': 'ripencc', 'prefix': '193.0.24.0/22', 'asn': 3333, 'max_len': 26, 'date_ranges': [['2017-01-14', '2018-12-27'], ['2019-01-03', '2019-06-24']]}
{'tal': 'ripencc', 'prefix': '193.0.24.0/24', 'asn': 3333, 'max_len': 24, 'date_ranges': [['2017-02-25', '2018-12-27'], ['2019-01-03', '2019-06-24']]}
{'tal': 'ripencc', 'prefix': '2001:610:240::/42', 'asn': 3333, 'max_len': 42, 'date_ranges': [['2015-03-10', '2016-01-26'], ['2016-01-30', '2018-12-27'], ['2019-01-03', '2019-10-21'], ['2019-10-23', '2020-02-23'], ['2020-02-25', '2020-04-05'], ['2020-04-07', '2020-08-02'], ['2020-08-04', '2021-04-21'], ['2021-04-23', '2021-04-24'], ['2021-04-28', '2022-02-26']]}
{'tal': 'ripencc', 'prefix': '2001:67c:2e8::/48', 'asn': 3333, 'max_len': 48, 'date_ranges': [['2015-03-10', '2016-01-26'], ['2016-01-30', '2018-12-27'], ['2019-01-03', '2019-10-21'], ['2019-10-23', '2020-02-23'], ['2020-02-25', '2020-04-05'], ['2020-04-07', '2020-08-02'], ['2020-08-04', '2021-04-21'], ['2021-04-23', '2021-04-24'], ['2021-04-28', '2022-02-26']]}
```

Available query fields:

- `Roas()`
  - `api_url`: the base URL for the BGPKIT ROAS instance. Default: `https://api.roas.bgpkit.com`
- `query()`
  - `prefix`: prefix to query in `str`
  - `asn`: AS number to query in `int`
  - `tal`: trust anchor to query in `str`, available values: `ripencc`, `arin`, `apnic`, `afrinic`, `lacnic`
  - `date`: date to query, format: `YYYY-MM-DD`, e.g. `2022-01-01`
  - `max_len`: filter results to only VRP's with specific max length
  - `debug`: boolean toggle to display debug information, default `False`
