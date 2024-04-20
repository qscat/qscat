<div align="center">

![qscat](https://github.com/upmsi-coaster/qscat/assets/58874676/fb40ffde-8667-48bc-99ba-1f8c4b257eb1)
[![QGIS (3.22.16)](https://github.com/louisfacun/qscat/actions/workflows/ci-3.22.16.yml/badge.svg)](https://github.com/louisfacun/qscat/actions/workflows/ci-3.22.16.yml)
[![QGIS (3.34.5)](https://github.com/louisfacun/qscat/actions/workflows/ci-3.34.5.yml/badge.svg)](https://github.com/louisfacun/qscat/actions/workflows/ci-3.34.5.yml)
[![QGIS (3.36.1)](https://github.com/louisfacun/qscat/actions/workflows/ci-3.36.1.yml/badge.svg)](https://github.com/louisfacun/qscat/actions/workflows/ci-3.36.1.yml)
[![codecov](https://codecov.io/gh/louisfacun/qscat/graph/badge.svg?token=37X4I6WRSY)](https://codecov.io/gh/louisfacun/qscat)
[![QGIS.org - 0.2.0](https://img.shields.io/badge/qgis.org-0.2.0-green.svg)](https://plugins.qgis.org/plugins/qscat)
[![Documentation Status](https://readthedocs.org/projects/qscat/badge/?version=latest)](https://qscat.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/780723777.svg)](https://zenodo.org/doi/10.5281/zenodo.10938766)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/louisfacun/qscat/badge)](https://securityscorecards.dev/viewer/?uri=github.com/louisfacun/qscat)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8758/badge)](https://www.bestpractices.dev/projects/8758)


<!--[![QGIS](https://img.shields.io/badge/qgis-3.22.*-green)](https://download.qgis.org/downloads/)-->

**QSCAT (QGIS Shoreline Change Analysis Tool)** is an open-source shoreline change analysis (SCA) tool for QGIS that builds upon the foundations set by [DSAS](https://www.usgs.gov/centers/whcmsc/science/digital-shoreline-analysis-system-dsas). It prioritizes speed, user-friendliness, and resource efficiency, making it a top choice for SCA research.

QSCAT was initially developed by UP-MSI CoastER team for a [government-funded initiative](https://research.mmsu.edu.ph/centers/coaster/) to establish coastal erosion trends in Region 1, Philippines. The team originally utilized DSAS for analysis but transitioned to QSCAT due to its enhanced features and capabilities. While we have yet to test QSCAT extensively in other regions, its design suggests potential applicability to various coastal areas.

</div>

## Features

QSCAT offers the following features:

* **Shoreline Change:** computes shoreline change statistics: shoreline change envelope (SCE), net shoreline movement (NSM), end-point rate (EPR), linear regression rate (LRR), and weighted linear regression rate (WLR).

* **Area Change:** calculates length and area of accreting, stable, and eroding coastal segments.

* **Forecasting:** predict future shoreline positions including uncertainty areas.

* **Automator:** tools that automate manual repetitive tasks.

* **Visualization:** shoreline and area change, forecasting results are visualized in the map for easy interpretation.

* **Summary Reports:** generates a comprehensive summary reports of the analysis results.

## Installation

<details open>
<summary>Plugins Repository</summary>

### Instructions

1. Open `QGIS`, `Plugins ‣ Manage and Install Plugins… ‣ Settings`.

2. Check `Show also experimental plugins`. Go to `All`.

3. Search `QGIS Shoreline Change Analysis Tool`.

4. Click `Install Plugin`.

5. Go to `Installed`. The `QGIS Shoreline Change Analysis Tool` should now appear in the list if the plugin is installed succesfuly. Check the checkbox to enable the plugin (if not checked).

6. Once enabled, the ![](/qscat/qscat.png) icon will appear in the toolbar.
   
</details>

<details open>
<summary>ZIP file</summary>

### Instructions

The latest QSCAT plugin is available as a ZIP file for installation. The steps to install the plugin on any operating system (Windows, Linux, Mac OS) are as follows:

1. Download the latest `qscat.zip` file from the following link: [https://github.com/louisfacun/qscat/releases/latest](https://github.com/louisfacun/qscat/releases/latest). OR `qscat-x.y-z.zip` from [https://plugins.qgis.org/plugins/qscat/](https://plugins.qgis.org/plugins/qscat/).

2. Open `QGIS`, `Plugins ‣ Manage and Install Plugins… ‣ Install from ZIP`.

3. Click `…`, find the downloaded `qscat.zip`, then click `Install Plugin`. Finally, proceed with the warning if asked.

4. Go to `Installed`. The `QGIS Shoreline Change Analysis Tool` should now appear in the list if the plugin is installed succesfuly. Check the checkbox to enable the plugin (if not checked).

5. Once enabled, the ![](/qscat/qscat.png) icon will appear in the toolbar.

</details>

See [QSCAT User Manual - Sample Workflow](https://qscat.readthedocs.io/en/latest/users_manual/others/sample_workflow.html) for sample usage.

## Resources
- [QSCAT User Manual](https://qscat.readthedocs.io)

## Contributing

We welcome contributions to QSCAT! Given that the plugin is in its initial stage, **bug reports are our top priority** as they help us identify and address issues to improve the stability and functionality of QSCAT. Whether it's code improvements, bug fixes, documentation enhancements, or translations, every contribution helps make QSCAT better for everyone. Please see our [Contribution Guide](CONTRIBUTING.md) for more details on how to get involved.

## License
- **[GPL License 3.0](LICENSE):** The QSCAT plugin is licensed under GPL 3.0, per [QGIS'](https://blog.qgis.org/2016/05/29/licensing-requirements-for-qgis-plugins/) Open Source Software principles. This decision aligns with the requirement for plugins to comply with GPL version 2 or greater for distribution through the QGIS plugin system.
