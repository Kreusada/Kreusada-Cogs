PYTHON ?= python3.8

# Python Code Style
reformat:
	$(PYTHON) -m isort --atomic --line-length 99 .
	$(PYTHON) -m black -l 99 .
stylecheck:
	$(PYTHON) -m isort --atomic --check --line-length 99 .
	$(PYTHON) -m black --check -l 99 .
stylediff:
	$(PYTHON) -m isort --atomic --check --diff --line-length 99 .
	$(PYTHON) -m black --check --diff -l 99 .
