# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../AlertService'))
sys.path.insert(0, os.path.abspath('../Common'))
sys.path.insert(0, os.path.abspath('../UserService'))
sys.path.insert(0, os.path.abspath('../ManagementService'))
sys.path.insert(0, os.path.abspath('../ReservationService'))

sys.path.insert(0, os.path.abspath('../AlertService/AlertAPI'))

sys.path.insert(0, os.path.abspath('../Common'))

sys.path.insert(0, os.path.abspath('../UserService/UserAPI'))

sys.path.insert(0, os.path.abspath('../ManagementService/ManagementAPI'))

sys.path.insert(0, os.path.abspath('../ReservationService/ReservationAPI'))


project = 'sejong-reservation'
copyright = '2023, chowchow0048'
author = 'chowchow0048'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']
autodoc_mock_imports = [
  "mariadb",
  "mysqlclient",
  "mysql",
  "SQLAlchemy",
  "pymysql"
 ]
  

templates_path = ['_templates']
exclude_patterns = []

root_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
