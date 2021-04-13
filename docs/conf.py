from sphinx.util.texescape import tex_replacements

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_context = {
    "display_github": True,
    "github_user": "Kreusada",
    "github_repo": "Kreusada-Cogs",
    "github_version": "master/docs/",
}

master_doc = 'index'

with open("prolog.txt", "r") as file:
    rst_prolog = file.read()

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = []
add_function_parentheses = True
project = u'Kreusada-Cogs'
copyright = u'2021 | Kreusada'
version = '' # Not versioning docs, lol
release = 'Alpha'