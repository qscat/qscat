# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2024-04-21

### Fixed

- Fix `Area Change Tab` visualization error.


## [0.3.0] - 2024-04-20

### Added

- Add checkbox to hide `Baseline orientation`.
- Add `Forecasting Tab` summary report.

### Changed

- Improve GUI icons design and made as SVGs for better quality.

### Fixed

- Fix `Forecasting Tab` transect layer input to display line string layer only, and show CRS.

## [0.2.0] - 2024-04-14

### Added

- Add `Summary Reports Tab` and enabling of individual reports for a dedicated summary reports setting.

### Changed

- Modify `Area Change Tab` to read newest and oldest date without requiring to `Update` from `Shoreline Change Tab`.
- Modify `Forecasting Tab` to input a transect layer.
- Move default summary reports location to user's home directory to prevent summary reports from getting deleted when the plugin is updated.
- Change file naming and foldering of summary reports to ``<computation>/qscat_<version>_<computation>_<datetime>.txt``
- Refactor and improve the majority of the codes. 
- Improve some parts of user manual (discussions and figures).

### Removed

- Remove version number in dock widget title for cleaner screenshots.

### Fixed

- Fix and refactor `update_newest_oldest_date()` function in `Shoreline Change Tab` > `Pairwise Comparison of Shorelines` now properly showing what is `newest` and `oldest` date.
- Fix `Transect Count` group box in `Transect Tab` not being enabled and disabled.
- Fix summary reports for `Shoreline Change Tab` not being generated.

## [0.1.0] - 2024-04-07

_First release_.
