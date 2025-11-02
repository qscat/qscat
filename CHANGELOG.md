# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.2] - 2025-11-02

### Fixed

- `Shoreline Change Tab`: Fixed `ZeroDivisionError` in calculation when preparing summary reports with no available data (classes and layers).

### Added

- Added `environment-3.36.1.yml` file for local development setup.
- Added local development setup instructions in `README.md`.

### Changed

- Improved documentation.

## [0.4.1] - 2024-07-18

### Fixed

- `Forecasting Tab`: Fixed issue on forecasting generating weird uncertainty points when date value of month was not 01.
- Fixed proper end time logging of shoreline change and forecasting.
- Minor bug fixes.

### Added

- `Visualization Tab`: Added option to select column, and input uncertainty value to support layers generated outside QSCAT.
- `Baseline Tab`, `Automator Tab`: Added smoothing distance field.
- `Shoreline Change Tab`, `Area Change Tab`, `Forecasting Tab`, `Visualization Tab`, `Summary Reports Tab`: Added input saving.
- `Help Tab`: Added useful links.
- `Shorelines Tab`: Added selected shorelines layer validation when changing layer selections.

### Changed

- `Shoreline Change Tab`: Made newest and oldest date selection automatic; no need for a button to update.
- Major code reformatting and refactoring.
- `User Manual`: Updated figures and texts.

## [0.4.0] - 2024-05-06

### Fixed

- `Visualization Tab`: Added missing stable class for SCE.
- `Visualization Tab`: Fixed Quantile and Jenks negative classification that included stable values.

### Added

- `Area Change Tab`: Added attributes for oldest shoreline length, average shoreline length, and mean shoreline displacement in area change vector layer output.
- `Area Change Tab`: Added oldest shoreline length and mean shoreline displacement in summary reports.
- Added QSCAT access to the plugin menu.
- Added transect cast, shoreline change, and forecasting execution time in QGIS message log.

### Changed

- Refactored and styled some codes using pylint, ruff, and black.
- UI: Updated labels for consistency.
- Docs: Improved some sections.

### Breaking Changes

- `Visualization Tab`: Improved UI and reading of input. This change required all previous stat layers to be regenerated.

## [0.3.1] - 2024-04-21

### Fixed

- Fixed `Area Change Tab` visualization error.
- Fixed `Forecasting Tab` error.

## [0.3.0] - 2024-04-20

### Added

- Added checkbox to hide `Baseline orientation`.
- Added `Forecasting Tab` summary report.

### Changed

- Improved GUI icons design and made as SVGs for better quality.

### Fixed

- Fixed `Forecasting Tab` transect layer input to display line string layer only, and show CRS.

## [0.2.0] - 2024-04-14

### Added

- Added `Summary Reports Tab` and enabling of individual reports for a dedicated summary reports setting.

### Changed

- Modified `Area Change Tab` to read newest and oldest date without requiring to `Update` from `Shoreline Change Tab`.
- Modified `Forecasting Tab` to input a transect layer.
- Moved default summary reports location to user's home directory to prevent summary reports from getting deleted when the plugin is updated.
- Changed file naming and foldering of summary reports to ``<computation>/qscat_<version>_<computation>_<datetime>.txt``
- Refactored and improved the majority of the code.
- Improved some parts of the user manual (discussions and figures).

### Removed

- Removed version number in dock widget title for cleaner screenshots.

### Fixed

- Fixed and refactored `update_newest_oldest_date()` function in `Shoreline Change Tab` > `Pairwise Comparison of Shorelines` now properly showing what is `newest` and `oldest` date.
- Fixed `Transect Count` group box in `Transect Tab` not being enabled and disabled.
- Fixed summary reports for `Shoreline Change Tab` not being generated.

## [0.1.0] - 2024-04-07


_First release_.
