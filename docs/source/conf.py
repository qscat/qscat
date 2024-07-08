# Configuration file for the Sphinx documentation builder.
# -- Project information

project = "QSCAT"
copyright = "2024, QSCAT"
author = """Louis Philippe Facun, Ma. Yvainne Sta. Maria, Rodel Ducao,
Jamela Jirah Clemente, Ellen Mae Carmelo, Angelo Maon,
Ara Rivina Malaya, Floribeth Cuison, and Fernando Siringan"""

latex_documents = [
    ('index', 'QSCAT.tex', 'QSCAT',
     'Louis Philippe Facun\\and Ma. Yvainne Sta. Maria\\and Rodel Ducao'
     '\\and Jamela Jirah Clemente\\and Ellen Mae Carmelo\\and Angelo Maon'
     '\\and Ara Rivina Malaya\\and Floribeth Cuison\\and and Fernando Siringan', 'manual'),
]

# latex_documents = [
#     ('index', 'QSCAT.tex', 'QSCAT',
#      'John Hunter\\and Darren Dale\\and Eric Firing\\and Michael Droettboom'
#      '\\and and the matplotlib development team', 'manual'),
# ]
latex_elements = {}
latex_elements['preamble'] = r"""
   % One line per author on title page
   \DeclareRobustCommand{\and}%
     {\end{tabular}\kern-\tabcolsep\\\begin{tabular}[t]{c}}%
   % In the parameters section, place a newline after the Parameters
   % header.  (This is stolen directly from Numpy's conf.py, since it
   % affects Numpy-style docstrings).
   \usepackage{expdlist}
   \let\latexdescription=\description
   \def\description{\latexdescription{}{} \breaklabel}
   \usepackage{amsmath}
   \usepackage{amsfonts}
   \usepackage{amssymb}
   \usepackage{txfonts}
   % The enumitem package provides unlimited nesting of lists and
   % enums.  Sphinx may use this in the future, in which case this can
   % be removed.  See
   % https://bitbucket.org/birkenfeld/sphinx/issue/777/latex-output-too-deeply-nested
   \usepackage{enumitem}
   \setlistdepth{2048}
"""
latex_elements['pointsize'] = '11pt'

release = "0.4.0"
version = "0.4.0"

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.bibtex",
    #"sphinx_sitemap",
    "sphinx_design",
    "sphinx_last_updated_by_git",
]

html_baseurl = "https://qscat.github.io/docs/latest/"
#itemap_url_scheme = "{link}"

# html_baseurl = "https://qscat.readthedocs.io/"
# sitemap_url_scheme = "{lang}latest/{link}"
# sitemap_excludes = [
#     "search.html",
#     "genindex.html",
# ]
#html_extra_path = ["robots.txt"]

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
            "url": "https://facebook.com/qscatplugin",
            "icon": "fa-brands fa-square-facebook",
        },
        {
            "name": "Twitter",
            "url": "https://twitter.com/qscatplugin",
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
    "article_footer_items": ["last-updated"],
}


html_title = f"{project}"
# html_title = f"{project} v{version}"
html_static_path = ["_static"]
html_sidebars = {"**": ["search-field", "sidebar-nav-bs", "sidebar-ethical-ads"]}
html_favicon = "favicon.ico"
html_last_updated_fmt = "%b %d, %Y" #%H:%M %z"
html_css_files = ["css/qscat.css"]

# -- Options for EPUB output
epub_show_urls = "footnote"

# Enable numeric figure references
numfig = True
numfig_secnum_depth = 2

# disable epub mimetype warnings
# https://github.com/sphinx-doc/sphinx/issues/10350#issuecomment-1484401954
suppress_warnings = ["epub.unknown_project_files"]
