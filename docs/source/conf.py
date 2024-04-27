# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'QSCAT'
copyright = '2024, QSCAT'
author = """Louis Facun, Fernando Siringan, Floribeth Cuison, Ara Rivina Malaya,
Ma. Yvainne Sta. Maria, Jamela Jirah Clemente, Angelo Maon, Ellen Mae Carmelo, 
and Rodel Ducao
"""

release = '0.3.1'
version = '0.3.1'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.bibtex',
]

# -- Bibtex configuration
bibtex_bibfiles = ['refs.bib']
bibtex_reference_style = 'author_year'

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -----------------------------------------------------------------------------
# HTML output
# -----------------------------------------------------------------------------

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "show_nav_level": 2,
    "logo": {
      "image_light": "_static/qscat-logo.svg",
      "image_dark": "_static/qscat-logo-dark.svg",
   },
   "external_links": [
      {"name": "GitHub", "url": "https://github.com/qscat/qscat"},
    ],
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
        }
    ],
}

html_title = "%s v%s Documentation" % (project, version)
html_static_path = ['_static']
html_sidebars = {'**': ['search-field', 'sidebar-nav-bs']}
html_favicon = "favicon.ico"
html_last_updated_fmt = '%Y %b %d, %H:%M %z'
html_css_files = ['css/qscat.css']
html_context = {"default_mode": "light"}

# -- Options for EPUB output
epub_show_urls = 'footnote'

# Enable numeric figure references
numfig = True
numfig_secnum_depth = 2

# disable epub mimetype warnings
# https://github.com/sphinx-doc/sphinx/issues/10350#issuecomment-1484401954
suppress_warnings = ["epub.unknown_project_files"]