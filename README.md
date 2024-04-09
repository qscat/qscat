![qscat](https://github.com/upmsi-coaster/qscat/assets/58874676/fb40ffde-8667-48bc-99ba-1f8c4b257eb1)

[![QGIS](https://img.shields.io/badge/qgis-3.22.*-green)](https://download.qgis.org/downloads/)
[![qgis plugin: 0.1.0](https://img.shields.io/badge/qgis_plugin-0.1.0-green.svg)](https://plugins.qgis.org/plugins/qscat)
[![License: GPL 3.0](https://img.shields.io/badge/license-GPL3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Documentation Status](https://readthedocs.org/projects/qscat/badge/?version=latest)](https://qscat.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/780723777.svg)](https://zenodo.org/doi/10.5281/zenodo.10938766)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/louisfacun/qscat/badge)](https://securityscorecards.dev/viewer/?uri=github.com/louisfacun/qscat)
<!-- [![codecov](https://codecov.io/gh/louisfacun/qscat/graph/badge.svg?token=37X4I6WRSY)](https://codecov.io/gh/louisfacun/qscat) -->
<!-- [![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/xxxx/badge)](https://bestpractices.coreinfrastructure.org/projects/xxxx) -->

<!-- QSCAT is an open-source shoreline change analysis tool for QGIS, builds upon the foundations set by DSAS. It prioritizes speed, accuracy, user-friendliness, and resource efficiency, establishing itself as a premier option for shoreline analysis research. -->

**QSCAT (QGIS' Shoreline Change Analysis Tool)** is an open-source shoreline change analysis tool for QGIS that builds upon the foundations set by [DSAS](https://www.usgs.gov/centers/whcmsc/science/digital-shoreline-analysis-system-dsas). It prioritizes speed, user-friendliness, and resource efficiency, making it a top choice for shoreline change analysis research.

QSCAT was initially developed by UP-MSI CoastER project 1 staff for a [government-funded initiative](https://research.mmsu.edu.ph/centers/coaster/) to establish coastal erosion trends in Region 1, Philippines. The team originally utilized DSAS for analysis but transitioned to QSCAT due to its enhanced features and capabilities. While we have yet to test QSCAT extensively in other regions, its design suggests potential applicability to various coastal areas.

## Installation

<details open>
<summary>By ZIP File</summary>

### Instructions

The latest QSCAT plugin is currently available as a ZIP file for installation. The steps to install the plugin on any operating system (Windows, Linux, Mac OS) are as follows:

1. Download the latest `qscat.zip` file from the following link: [https://github.com/louisfacun/qscat/releases/latest](https://github.com/louisfacun/qscat/releases/latest)

2. Open `QGIS`, `Plugins ‣ Manage and Install Plugins… ‣ Install from ZIP`.

3. Click `…`, find the downloaded `qscat.zip`, then click `Install Plugin`. Finally, proceed with the warning if asked.

4. Go to `Installed`. The `QGIS' Shoreline Change Analysis Tool` should now appear in the list if the plugin is installed succesfuly. Check the checkbox to enable the plugin (if not checked).

5. Once enabled, the `QSCAT icon` plugin will appear in the toolbar.

</details>

## Resources
- [QSCAT User Manual](https://qscat.readthedocs.io)

## License
- **[GPL License 3.0](LICENSE):** The QSCAT plugin is licensed under GPL 3.0, per [QGIS'](https://blog.qgis.org/2016/05/29/licensing-requirements-for-qgis-plugins/) Open Source Software principles. This decision aligns with the requirement for plugins to comply with GPL version 2 or greater for distribution through the QGIS plugin system.
