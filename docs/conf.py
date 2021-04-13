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