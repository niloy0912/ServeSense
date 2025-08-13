import os
import sys
import django

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath(".."))  # Go up one directory from docs/
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Serve_Sense_DB.settings")
django.setup()

# -- Project information -----------------------------------------------------
project = 'Serve Sense'
copyright = '2025, Tamjid'
author = 'Tamjid'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",      # Automatically document docstrings
    "sphinx.ext.viewcode",     # Add links to source code
    "sphinx.ext.napoleon",     # Support for Google/NumPy style docstrings
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
