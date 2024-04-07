# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'QSCAT'
copyright = '2024, UP-MSI COASTER Team'
author = 'UP-MSI COASTER Team'

release = '1.0.0'
version = '1.0.0'

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

# -- Options for HTML output
html_theme = 'sphinx_rtd_theme'

# These folders are copied to the documentation's HTML output
html_static_path = ['_static']
# html_theme_options = {
#     'logo_only': True,
#     'display_version': False,
# }
# html_logo = "qscat-logo.svg"
html_last_updated_fmt = '%Y %b %d, %H:%M %z'

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/custom.css',
]

# -- Options for EPUB output
epub_show_urls = 'footnote'

# Enable numeric figure references
numfig = True
numfig_secnum_depth = 2