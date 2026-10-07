# Changelog

All notable changes to this project will be documented in this file.

## v0.9.0 - 2026-10-07

### Highlights

* Fix `Broker.latest()`, `Broker.peers()`, and `Broker.collectors()` against the current v3 API: latest items parse their per-item `delay`, peer and collector items match the v3 response shapes, and pagination no longer loops on endpoints that ignore page parameters ([#13](https://github.com/bgpkit/pybgpkit/pull/13)).
* Fix the remaining clients: `AsnLookup` parses the nested v3 items and starts at the 0-indexed `page`, `CommunityLookup` flattens the per-ASN community lists and reads the `sources` key, and `Roas` targets the v3 endpoint and paginates ([#13](https://github.com/bgpkit/pybgpkit/pull/13)).
* Add `BGPKITApiError` for all request failures and shared helpers in `bgpkit/_utils.py`; `Broker` honors the `BGPKIT_BROKER_URL` environment variable ([#13](https://github.com/bgpkit/pybgpkit/pull/13)).
* Add unit tests for every client and a `Tests` workflow that runs them on push and pull requests; `PeerItem`, `CollectorItem`, and `AsnInfo` field sets now match the v3 API responses ([#13](https://github.com/bgpkit/pybgpkit/pull/13)).

## v0.8.0 - 2026-07-02

### Highlights

* Update `pybgpkit-parser` dependency to `>=0.18.0`.

## v0.7.0 - 2026-06-09

### Highlights

* Update `pybgpkit-parser` dependency to `>=0.7.0`.
* Add `RouteParser`, `RouteElem`, and `Filter` re-exports from `pybgpkit-parser`.
* Modernize packaging to PEP 621 `pyproject.toml`.
* Fix Broker default API URL (`api.bgpkit.com/broker` → `api.bgpkit.com/v3/broker`).
* Add Broker `latest()`, `peers()`, and `collectors()` methods.
* Add `IpLookup` for IP address lookup (v3/utils/ip).
* Add `AsnLookup` for ASN information lookup (v3/utils/asn).
* Add `CommunityLookup` for BGP community queries and source listing.
* Remove unused `dataclasses_json` dependency.
* Add automated PyPI publishing via GitHub Actions and Trusted Publishing.
* Move tests into `tests/` directory.
