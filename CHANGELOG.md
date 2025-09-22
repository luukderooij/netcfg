# CHANGELOG

<!-- version list -->

## v1.2.0 (2025-09-22)

### Features

- Restructure GUI by creating separate tab classes and removing old gui.py
  ([`fd28534`](https://github.com/luukderooij/netcfg/commit/fd28534a5b0cec1278cd6008a5544da349defe05))


## v1.1.0 (2025-09-14)

### Features

- Add Ping functionality to GUI and implement ping command in new ping.py module
  ([`4321dd6`](https://github.com/luukderooij/netcfg/commit/4321dd6309dac427d6c555c45bb93410881967da))

- Load changelog from CHANGELOG.md instead of changelog.py
  ([`b2eb739`](https://github.com/luukderooij/netcfg/commit/b2eb739a889abbb39c279cc21c51df479f69af8f))

### Refactoring

- Remove changelog.py and its import from gui.py
  ([`740a50c`](https://github.com/luukderooij/netcfg/commit/740a50cb68d87d0e73944894d60830f0eef431cf))


## v1.0.1 (2025-09-11)

### Bug Fixes

- Version retrieval in GUI by loading from pyproject.toml or fallback to metadata
  ([`18e5c7c`](https://github.com/luukderooij/netcfg/commit/18e5c7c5d6d95107d7e8c23abcdf213e81815890))


## v1.0.0 (2025-09-10)

- Initial Release
