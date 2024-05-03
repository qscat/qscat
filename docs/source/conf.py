# Configuration file for the Sphinx documentation builder.

# -- Project information

project = "QSCAT"
copyright = "2024, QSCAT"
author = """Louis Facun, Fernando Siringan, Floribeth Cuison, Ara Rivina Malaya,
Ma. Yvainne Sta. Maria, Jamela Jirah Clemente, Angelo Maon, Ellen Mae Carmelo, 
and Rodel Ducao
"""

release = "0.3.1"
version = "0.3.1"

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.bibtex",
    "sphinx_sitemap",
    "sphinx_design",
]

# html_baseurl = "https://qscat.github.io/docs/"
# sitemap_url_scheme = "{link}"

html_baseurl = "https://qscat.readthedocs.io/"
sitemap_url_scheme = "{lang}latest/{link}"
sitemap_excludes = [
    "search.html",
    "genindex.html",
]
html_extra_path = ['robots.txt']

# -- Bibtex configuration
bibtex_bibfiles = ["refs.bib"]
bibtex_reference_style = "author_year"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -----------------------------------------------------------------------------
# HTML output
# -----------------------------------------------------------------------------

html_theme = "pydata_sphinx_theme"

html_context = {
    "default_mode": "light",
    "github_user": "qscat",
    "github_repo": "qscat",
    "github_version": "master",
    "doc_path": "docs/source",
}

html_theme_options = {
    "show_nav_level": 1,
    "logo": {
        "image_light": "_static/qscat-logo.svg",
        "image_dark": "_static/qscat-logo-dark.svg",
    },
    # "external_links": [
    #     {"name": "GitHub", "url": "https://github.com/qscat/qscat"},
    # ],
    "icon_links": [
        {
            "name": "Facebook",
            "url": "https://facebook.com/QSCATplugin",
            "icon": "fa-brands fa-square-facebook",
        },
        {
            "name": "Twitter",
            "url": "https://twitter.com/QSCATplugin",
            "icon": "fa-brands fa-square-twitter",
        },
    ],
    "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
    "footer_start": ["copyright", "sphinx-version"],
    "footer_end": [],
    "use_edit_page_button": True,
    "github_url": "https://github.com/qscat/qscat",
    "show_version_warning_banner": True,
    # "primary_sidebar_end": ["indices.html", "sidebar-ethical-ads.html"],
    # #"content_footer_items": ["last-updated"],
    # "switcher": {
    #     "json_url": "switcher.json",
    # }
}


html_title = f"{project} v{version}"
html_static_path = ["_static"]
html_sidebars = {"**": ["search-field", "sidebar-nav-bs", "sidebar-ethical-ads"]}
html_favicon = "favicon.ico"
html_last_updated_fmt = "%Y %b %d, %H:%M %z"
html_css_files = ["css/qscat.css"]

# -- Options for EPUB output
epub_show_urls = "footnote"

# Enable numeric figure references
numfig = True
numfig_secnum_depth = 2

# disable epub mimetype warnings
# https://github.com/sphinx-doc/sphinx/issues/10350#issuecomment-1484401954
suppress_warnings = ["epub.unknown_project_files"]
