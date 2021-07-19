PYTHON ?= python3.8

# Python Code Style
reformat:
	$(PYTHON) -m isort .
	$(PYTHON) -m black .

gettext:
	redgettext --command-docstrings --verbose --recursive --exclude-files "docs/*" --exclude-files "instantcmd/*" .

upload_translations:
	crowdin upload sources

download_translations:
	crowdin download
