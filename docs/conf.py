exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".venv", "venv"]
html_css_files = ["literals.css"]
extensions = ["sphinx_rtd_theme"]
templates_path = ["_templates"]

html_context = {
    "display_github": True,
    "github_user": "Kreusada",
    "github_repo": "Kreusada-Cogs",
    "github_version": "master/docs/",
}

master_doc = "index"
html_theme = "furo"
source_suffix = ".rst"
master_doc = "index"
exclude_patterns = []
add_function_parentheses = True

project = "Kreusada-Cogs"
copyright = "2020 - 2023 | Kreusada"
html_logo = "image_cog-creators-logo.png"
