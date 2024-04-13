# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add `Summary Reports Tab` and enabling of individual reports for a dedicated summary reports setting.

### Changed

- Modify `Area Change Tab` to read newest and oldest date withot requiring to `Update` from `Shoreline Change Tab`.
- Move default summary reports location to user's home directory to prevent summary reports getting deleted when the plugin is updated.
- Change file naming and foldering of summary reports to ``<computation>/qscat_<version>_<computation>_<datetime>.txt``
- Refactor and improve majority of the codes. 
- Improve some parts of user manual (discussions and figures).

### Removed

- Remove version number in dock widget title for cleaner screenshots.

### Fixed

- Fix and refactor `update_newest_oldest_date()` function in `Shoreline Change Tab` > `Pairwise Comparison of Shorelines` now properly showing what is `newest` and `oldest` date.
- Fix `Transect Count` group box in `Transect Tab` not being enabled and disabled.
- Fix summary reports for `Shoreline Change Tab` not being generated.

### TODO

- Add `Shoreline Change Tab` input parameters saving.
- Add area change, forecasting, summary reports, parameter saving
- Add area change own transect layer and newest nsm selection?
- Refactor inconsistent object naming.
- Refactor statistics params to shoreline change params.


## [0.1.0] - 2024-04-07

_First release_.