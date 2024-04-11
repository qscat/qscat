# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add `Summary Reports Tab` and enabling of individual reports for a dedicated summary reports setting.

### Changed

- Move default summary reports location to user's home directory to prevent summary reports getting deleted when the plugin is updated.
- Change file naming and foldering of summary reports to ``<computation>/qscat_<version>_<computation>_<datetime>.txt``
- Improve documentation of function `get_shorelines_dates()`.
- Improve some parts of user manual (discussions and figures).

### Removed

- Remove version number in dockwidget title for cleaner screenshots.

### Fixed

- Fix and refactor `update_newest_oldest_date()` function in `Shoreline Change Tab` > `Pairwise Comparison of Shorelines` now properly showing what is `newest` and `oldest` date.
- Fix `Transect Count` group box in `Transect Tab` not being enabled and disabled.
- Fix summary reports for `Shoreline Change Tab` not being generated.

### TODO

- Fix unchecked `Clip transects` in `Shoreline Change Tab` not working.
- Add `Shoreline Change Tab` input parameters saving.
- Refactor inconsistent object naming.
- Refactor statistics params to shoreline change params.

## [0.1.0] - 2024-04-07

_First release_.