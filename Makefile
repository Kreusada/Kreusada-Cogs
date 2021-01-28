PYTHON ?= python3.8

# Python Code Style
reformat:
	$(PYTHON) -m isort --atomic --line-length 99 .
	$(PYTHON) -m black -l 99 .
