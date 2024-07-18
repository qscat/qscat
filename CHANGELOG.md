# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.2] - Unreleased

### TODO

- `Forecasting Tab`: Offers forecasting options from transects layer or from LRR layer.
- `Forecasting Tab`: Improve forecasting input; currently it depends on shoreline change inputs such newest and oldest date, and transect-shoreline intersections.


## [0.4.1] - 2024-07-18

### Fixed

- `Forecasting Tab`: Fix issue on forecasting generating weird uncertainty points when date value of month is not 01.
- Fix proper end time logging of shoreline change and forecasting.
- Minor bug fixes.

### Added

- `Visualization Tab`: Add option to select column, and input uncertainty value to support layers generated outside QSCAT.
- `Baseline Tab`, `Automator Tab`: Add smoothing distance field.
- `Shoreline Change Tab`, `Area Change Tab`, `Forecasting Tab`, `Visualization Tab`, `Summary Reports Tab`: Add input saving.
- `Help Tab`: Add useful links.
- `Shorelines Tab`: Add selected shorelines layer validation when changing layer selections.

### Changed

- `Shoreline Change Tab`: Make newest and oldest date selection automatic; no need to button to update.
- Major code reformatting and refactor.
- `User Manual`: Update figures and texts.

## [0.4.0] - 2024-05-06

### Fixed

- `Visualization Tab`: Add missing stable class for SCE.
- `Visualization Tab`: Fix Quantile and Jenks negative classification that includes stable values.

### Added

- `Area Change Tab`: Add attributes for oldest shoreline length, average shoreline length, and mean shoreline displacement in area change vector layer output.
- `Area Change Tab`: Add oldest shoreline length and mean shoreline displacement in summary reports.
- Add QSCAT access to the plugin menu.
- Add transect cast, shoreline change, and forecasting execution time in QGIS message log.

### Changed

- Refactor and style some codes using pylint, ruff, and black.
- UI: Update labels for consistency.
- Docs: Improve some sections.

### Breaking Changes

- `Visualization Tab`: Improved UI and reading of input. This change requires all previous stat layers to be regenerated.

## [0.3.1] - 2024-04-21

### Fixed

- Fix `Area Change Tab` visualization error.
- Fix `Forecasting Tab` error.

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
