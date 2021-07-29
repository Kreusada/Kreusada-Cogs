PYTHON ?= python3.8

# Python Code Style
reformat:
	$(PYTHON) -m isort .
	$(PYTHON) -m black .
