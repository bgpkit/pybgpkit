# Changelog

All notable changes to this project will be documented in this file.

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
