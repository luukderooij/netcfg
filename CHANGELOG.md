# CHANGELOG

<!-- version list -->

## v1.5.0 (2025-10-01)

### Features

- Add methods to open Npcap download page and retrieve download URL in ArpScanner
  ([`8ae89bf`](https://github.com/luukderooij/netcfg/commit/8ae89bfcb7b709bdab3719b7026b8ec08eef4bfc))

### Refactoring

- Add interface selection to ArpScanner and update ArpScanTab to use last selected adapter
  ([`fae0e14`](https://github.com/luukderooij/netcfg/commit/fae0e142096984156a14b7873fc4dc596cf7bd19))

- Add logging configuration to main execution block
  ([`3c34e9c`](https://github.com/luukderooij/netcfg/commit/3c34e9c4761f4e6d96b822e27a33e3f8bf0ee43e))

- Enhance logging and simplify docstrings in ArpScanner
  ([`45ccb97`](https://github.com/luukderooij/netcfg/commit/45ccb9714b388cca4d49b70b7a1daa54f3a968d5))

- Initialize settings management with load and save functions
  ([`19b3df4`](https://github.com/luukderooij/netcfg/commit/19b3df44f0259ec64f1cbecb528192f3b83e009a))

- Remove commented-out code and clean up main execution block
  ([`7923eaa`](https://github.com/luukderooij/netcfg/commit/7923eaa2bc40e7a2d7ad07da5fd87204097978b8))

- Remove version import from __init__.py
  ([`6bcc7ad`](https://github.com/luukderooij/netcfg/commit/6bcc7ad69431f223542ccb8f4609a67ae37e9c50))

- Update ConfigTab to save and restore last selected adapter
  ([`ccbeac7`](https://github.com/luukderooij/netcfg/commit/ccbeac762e98d5e776b6f3e25e901c6748933c8b))


## v1.4.0 (2025-09-27)

### Features

- Implement automatic configuration refresh in ConfigTab
  ([`b1d7761`](https://github.com/luukderooij/netcfg/commit/b1d77618c4900b57ba63c572e01e735ab760413d))


## v1.3.0 (2025-09-27)

### Features

- Add ARP scanning functionality with GUI integration
  ([`f54f4c8`](https://github.com/luukderooij/netcfg/commit/f54f4c83f9376b151cc9c12a7f85548171abdd57))


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
