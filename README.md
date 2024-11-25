<div align="center">
   
![QSCAT logo](https://github.com/qscat/qscat/assets/58874676/fefa611f-c4a9-4551-979d-1c3b193d38ea)


[![QGIS](https://img.shields.io/badge/qgis-3.22.16_|_3.34.5_|_3.36.1-green)](https://download.qgis.org/downloads/)
[![QGIS.org - 0.4.1](https://img.shields.io/badge/qgis.org-0.4.1-green.svg)](https://plugins.qgis.org/plugins/qscat)
[![DOI](https://zenodo.org/badge/780723777.svg)](https://zenodo.org/doi/10.5281/zenodo.10938766)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/qscat/qscat/badge)](https://securityscorecards.dev/viewer/?uri=github.com/qscat/qscat)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8758/badge)](https://www.bestpractices.dev/projects/8758)


**QSCAT (QGIS Shoreline Change Analysis Tool)** is an open-source shoreline change analysis (SCA) tool for QGIS that builds upon the foundations set by [DSAS](https://www.usgs.gov/centers/whcmsc/science/digital-shoreline-analysis-system-dsas). It prioritizes speed, user-friendliness, and resource efficiency, making it a top choice for SCA research.

QSCAT was initially developed by UP-MSI CoastER team for a [government-funded initiative](https://research.mmsu.edu.ph/centers/coaster/) to establish coastal erosion trends in Region 1, Philippines. The team originally utilized DSAS for analysis but transitioned to QSCAT due to its enhanced features and capabilities. While we have yet to test QSCAT extensively in other regions, its design suggests potential applicability to various coastal areas.

</div>

![qscat](https://github.com/qscat/qscat/assets/58874676/df5f0bb2-ce42-4270-bf01-7d4f01d58ae6)

## Warning

QSCAT is currently unstable, so please expect for potential bugs and issues. In the meantime, we kindly request your assistance in reporting any problems you encounter at QSCAT GitHub Issues (https://github.com/qscat/qscat/issues). Thank you for your cooperation!


## QGIS versions compatibility

| Name  | Status |
| - | - |
| test coverage (ongoing) | [![codecov](https://codecov.io/gh/qscat/qscat/graph/badge.svg?token=37X4I6WRSY)](https://codecov.io/gh/qscat/qscat) |
| **3.22.16** | [![QGIS (3.22.16)](https://github.com/qscat/qscat/actions/workflows/ci-3.22.16.yml/badge.svg)](https://github.com/qscat/qscat/actions/workflows/ci-3.22.16.yml) |
| **3.34.5** | [![QGIS (3.34.5)](https://github.com/qscat/qscat/actions/workflows/ci-3.34.5.yml/badge.svg)](https://github.com/qscat/qscat/actions/workflows/ci-3.34.5.yml) |
| **3.36.1**| [![QGIS (3.36.1)](https://github.com/qscat/qscat/actions/workflows/ci-3.36.1.yml/badge.svg)](https://github.com/qscat/qscat/actions/workflows/ci-3.36.1.yml) |

## Features

QSCAT offers the following features:

| Feature | Description |
| - | -- |
| [**Shoreline Change**](https://qscat.github.io/docs/latest/manual/tabs/shoreline_change.html) | Computes shoreline change statistics: shoreline change envelope (SCE), net shoreline movement (NSM), end-point rate (EPR), linear regression rate (LRR), and weighted linear regression rate (WLR). |
| [**Area Change**](https://qscat.github.io/docs/latest/manual/tabs/area_change.html) | Calculates length and area of accreting, stable, and eroding coastal segments. |
| [**Forecasting**](https://qscat.github.io/docs/latest/manual/tabs/forecasting.html) | Predicts future shoreline positions including uncertainty areas. |
| [**Automator**](https://qscat.github.io/docs/latest/manual/tabs/automator.html) | Automates manual repetitive tasks. |
| [**Visualization**](https://qscat.github.io/docs/latest/manual/tabs/visualization.html) | Visualizes shoreline and area change, forecasting results in the map for easy interpretation. |
| [**Summary Report**](https://qscat.github.io/docs/latest/manual/tabs/summary_reports.html) | Generates a comprehensive summary report of the results. |

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

1. Download the latest `qscat.zip` file from the following link: [https://github.com/qscat/qscat/releases/latest](https://github.com/qscat/qscat/releases/latest). OR `qscat-x.y-z.zip` from [https://plugins.qgis.org/plugins/qscat/](https://plugins.qgis.org/plugins/qscat/).

2. Open `QGIS`, `Plugins ‣ Manage and Install Plugins… ‣ Install from ZIP`.

3. Click `…`, find the downloaded `qscat.zip`, then click `Install Plugin`. Finally, proceed with the warning if asked.

4. Go to `Installed`. The `QGIS Shoreline Change Analysis Tool` should now appear in the list if the plugin is installed succesfuly. Check the checkbox to enable the plugin (if not checked).

5. Once enabled, the ![](/qscat/qscat.png) icon will appear in the toolbar.

</details>

See [QSCAT User Manual - Sample Workflow](https://qscat.github.io/docs/latest/manual/others/sample_workflow.html) for sample usage.

## Resources
- [QSCAT Website](https://qscat.github.io)
- [QSCAT Documentation](https://qscat.github.io/docs/latest)
- [QSCAT User Manual](https://qscat.github.io/docs/latest/manual)
- [QSCAT Facebook Page](https://web.facebook.com/qscatplugin)
- [QSCAT Facebook Group](https://web.facebook.com/groups/qscat)
- [QSCAT Twitter](https://twitter.com/qscatplugin)
  
## Contributing

- We welcome contributions to QSCAT! Given that the plugin is in its initial stage, **bug reports are our top priority** as they help us identify and address issues to improve the stability and functionality of QSCAT. Whether it's code improvements, bug fixes, documentation enhancements, or translations, every contribution helps make QSCAT better for everyone. Please see our [Contribution Guide](CONTRIBUTING.md) for more details on how to get involved.

## License
- **[GPL License 3.0](LICENSE):** The QSCAT plugin is licensed under GPL 3.0, per [QGIS'](https://blog.qgis.org/2016/05/29/licensing-requirements-for-qgis-plugins/) Open Source Software principles. This decision aligns with the requirement for plugins to comply with GPL version 2 or greater for distribution through the QGIS plugin system.

## Citation

If you use our work, please consider citing it as below:

Facun, L. P., Sta Maria, M. Y., Ducao, R., Clemente, J. J., Carmelo, E. M., Maon, A., Malaya, A. R., Cuison, F., & Siringan, F. (2024). QGIS Shoreline Change Analysis Tool (QSCAT): A fast, open-source shoreline change analysis plugin for QGIS. *Environmental Modelling & Software*, 136, 106263. https://doi.org/10.1016/j.envsoft.2024.106263


**BibTeX Entry**

```bibtex
@article{FACUN2024106263,
  title = {QGIS Shoreline Change Analysis Tool (QSCAT): A fast, open-source shoreline change analysis plugin for QGIS},
  journal = {Environmental Modelling & Software},
  pages = {106263},
  year = {2024},
  issn = {1364-8152},
  doi = {https://doi.org/10.1016/j.envsoft.2024.106263},
  url = {https://www.sciencedirect.com/science/article/pii/S1364815224003244},
  author = {Louis Philippe Facun and Ma. Yvainne {Sta Maria} and Rodel Ducao and Jamela Jirah Clemente and Ellen Mae Carmelo and Angelo Maon and Ara Rivina Malaya and Floribeth Cuison and Fernando Siringan},
  keywords = {Coastal erosion, Geographic information systems, Open-source software, Shoreline change analysis},
  abstract = {Coastal erosion poses a significant threat to most coastal communities. This necessitates a better understanding of coastal erosion dynamics, and thus, shoreline change analysis (SCA) tools would be handy. However, many available tools require commercial softwares and/or a faster computing platform. To address these issues, QGIS’ Shoreline Change Analysis Tool (QSCAT), a new QGIS plugin built with Python, was developed. QSCAT can perform transect-based and area-based analyses. The transect-based algorithm of QSCAT was patterned after the Digital Shoreline Analysis System (DSAS). Whereas, the area-based algorithm is similar to the change polygon method. Running QSCAT and DSAS together demonstrated that QSCAT generated the same results as DSAS but its overall speed is 8 times faster than DSAS. QSCAT can estimate beach area loss and length of eroding shorelines, which can identify erosion hotspots. These features attest to QSCAT’s potential as a more efficient and an equally reliable SCA tool.}
}
