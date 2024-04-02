# Changelog

## Released
## 1.1.2-beta - June 14, 2023
### Added
- Added checkbox on GUI to quickly select and select shoreline change statistics.

### Fixed 
- Shoreline change statistics proper signs are now fixed.

## 1.1.1-beta - June 5, 2023
### Added
- Added plugin auto download and install functionality.

### Changed
- Changed shoreline forecasting to background tasks (prevent QGIS freezing).

### Fixed 
- Fixed `WLR` weights.

## 1.1.0-beta - May 31, 2023
### Added
- Added shoreline forecasting using `Kalman Filter`.
- Added `LSE` and `LCI`  to `LRR` computation.
- Added `Confidence Interval (%)` supplemental parameter for `LCI`.
  
### Fixed
- Date `MM/YYYY` conversion to decimal year `YYYY.YY` computation.

## 1.0.8-beta - May 25, 2023
### Fixed
- Fixed `SCE`, `LRR`, `WLR` signs.

## 1.0.7-beta - May 6, 2023
### Added
- Added `Weighted Linear Regression (WLR)` computation ([#26](/../../issues/26)).
  
### Changed
- Modified summary report for shoreline change ([#25](/../../issues/25)).
  
## 1.0.6-beta - April 24, 2023
### Fixed
- Fixed complex shoreline ([#18](/../../issues/18)).

## 1.0.5-beta - April 22, 2023
### Added
- Added `stable` to `EPR_trend` ([#5](/../../issues/5)).
- Added `SCE_trend` to `SCE` ([#19](/../../issues/19)).
- Added `LRR` pre-checks to atleast 3 shorelines ([#17](/../../issues/17)).
- Added summary reports file ([#21](/../../issues/21)).

### Changed
- Changed `NSM_type` to `NSM_trend` ([#12](/../../issues/12)).
- Changed update checking to `About` Tab.

### Fixed
- Fixed `default data uncertainty` ([#15](/../../issues/15)).

## 1.0.4-beta - April 14, 2023
### Added
- Added support to calculate areas with "river" shorelines with one polygon area - without dividing the area ([#7](/../../issues/7)).
- Added feature to check latest updates and notify.

### Changed
- Changed some GUI texts ([#13](/../../issues/13)).

## 1.0.3-beta - March 31, 2023
### Fixed
- Fixed variable typo: error when calculating area.

## 1.0.2-beta - March 29, 2023
### Changed
- Changed `Transects Tab` label headings.

### Fixed
- Fixed `Transects Tab` > `Choose by Distance` > not working `Closest` selection.
- Fixed `Transects Tab` > `Choose by Distance` and `Choose by Placement` can check two options (radio button) at the same time.

## 1.0.1-beta - March 27, 2023
### Added
- Added `Update` button to populate newest and oldest year choices ([#2](/../../issues/2)).
- Added pre-check step before casting transect: save the project first ([#3](/../../issues/3)).

### Changed
- Modified UI of `Statistics Tab` > `Additional Parameters` > `For NSM and EPR` way of populating choices. Now requires clicking the `Update` button.

### Fixed
- Fixed populating newest and oldest year choices error affecting other plugin functions such as `Automator Tab` ([#2](/../../issues/2)).

## 1.0.0-beta - March 20, 2023
Initial release of QSCAT for beta testing.
