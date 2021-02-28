import sphinx_rtd_theme

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "Kreusada-Cogs"
copyright = "Kreusada (2021)"
author = "Kreusada"

extensions = ["sphinx_rtd_theme"]
templates_path = ["_templates"]
exclude_patterns = ["_build"]
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]