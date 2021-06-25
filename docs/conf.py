# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../TCalc'))




# -- Project information -----------------------------------------------------

project = 'TCalc: Telescope-Calculator'
copyright = '2021, Bhavesh Rajpoot, Ryan Keenan, Binod Bhattarai, Dylon Benton'
author = 'Bhavesh Rajpoot, Ryan Keenan, Binod Bhattarai, Dylon Benton'
master_doc='index'

# The full version, including alpha/beta/rc tags
release = "1.0.2"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc",
            "sphinx.ext.napoleon",
            "sphinx.ext.mathjax", 
            "sphinx-mathjax-offline",
            'sphinx.ext.autosummary', 
            'sphinx_autopackagesummary',
            "seed_intersphinx_mapping"]

autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'sphinx_rtd_theme'
# html_theme = 'press'
# html_theme = 'insegel'
html_theme = "pydata_sphinx_theme" #theme use by numpy, pandas, etc

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# for adding logo on docs page
# html_logo = "_static/logo.png"

# custom icon links
html_theme_options = {
      "external_links": [
    #   {"name": "link-one-name", "url": "https://<link-one>"},
    #   {"name": "link-two-name", "url": "https://<link-two>"}
      ],
    "icon_links": [{
            "name": "GitHub",
            "url": "https://github.com/Bhavesh012/Telescope-Calculator",
            "icon": "fab fa-github-square",}
            ],
    "use_edit_page_button": True,
    "page_sidebar_items": ["page-toc", "edit-this-page", "search-field"],
    "footer_items": ["copyright", "sphinx-version"],

}

html_context = {
    # "github_url": "https://github.com", # or your GitHub Enterprise interprise
    "github_user": "Bhavesh Rajpoot",
    "github_repo": "Telescope-Calculator",
    "github_version": "main",
    "doc_path": ".\docs",
}


# intersphinx enables links to classes/functions in the packages defined here:
intersphinx_mapping = {'python': ('https://docs.python.org/3/', None),
                       'numpy': ('https://docs.scipy.org/doc/numpy/', None),
                       'matplotlib': ('https://matplotlib.org', None),}
