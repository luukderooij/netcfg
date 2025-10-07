# CHANGELOG

<!-- version list -->

## v1.6.0 (2025-10-07)

### Bug Fixes

- Add requires-python field to specify Python version requirement
  ([`4164ff3`](https://github.com/luukderooij/netcfg/commit/4164ff3f8856abc2fe9773b96b4467f03d41ca0d))

- Simplify error message for Npcap requirement in ARP scanning
  ([`6ca7d05`](https://github.com/luukderooij/netcfg/commit/6ca7d055ae01087275ba7500bff30f926cbb22f1))

- Update script to correctly reference main.py in netcfg folder
  ([`8e2e046`](https://github.com/luukderooij/netcfg/commit/8e2e046a744aa4aa6b8dc6b3487b70889740a368))

### Features

- Implement Pinger class for enhanced ping functionality and GUI integration
  ([`da58a2d`](https://github.com/luukderooij/netcfg/commit/da58a2d82227f520b46e1cf5a0b8b459dec05236))

- Moved main.py file to netcfg folder.
  ([`26a49ac`](https://github.com/luukderooij/netcfg/commit/26a49ac8079cc0f7c2abcd786673b77fc642bd02))

### Refactoring

- Clean up whitespace and formatting in PingTab class
  ([`d321e70`](https://github.com/luukderooij/netcfg/commit/d321e70158b7f60743e8054a1ce0f9ffc6fb8ce2))

- Improve layout and padding in PingTab UI components
  ([`4e4842f`](https://github.com/luukderooij/netcfg/commit/4e4842fa307eff6ad9cff7258e35b9d3937febc7))

- Moved files to diffent folders for better structure.
  ([`56f5805`](https://github.com/luukderooij/netcfg/commit/56f58059eddcb7ec61e8ee01a11f9d6afd18c248))

- Remove unused run_ping and main functions from ping.py
  ([`789a2db`](https://github.com/luukderooij/netcfg/commit/789a2dbacbe9cda119890bc4f5719b77864982fc))

- Update import statements to simplify module paths
  ([`64bdc03`](https://github.com/luukderooij/netcfg/commit/64bdc0306da3701c686bccafbe5510dda41f5726))


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
