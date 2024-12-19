# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "DocrepoX"
copyright = "2024, Documendous LLC"
author = "Documendous LLC"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = []

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
# html_theme = 'furo'
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

extensions = [
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]

extensions.append("sphinx.ext.intersphinx")
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "django": ("https://docs.djangoproject.com/en/stable/", None),
}


autoapi_type = "python"
autoapi_dirs = ["../docrepo"]  # Path to your Python source code

# html_theme_options = {
#     'navigation_depth': 4,
# }

html_show_sourcelink = True
pygments_style = "sphinx"  # Try 'monokai' or 'friendly' for a different look

html_title = "DocrepoX Docs"

extensions.append("sphinx_copybutton")

html_sidebars = {"**": ["globaltoc.html", "searchbox.html"]}
