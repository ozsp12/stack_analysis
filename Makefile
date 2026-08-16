PYTHON ?= python

.PHONY: install install-dev lint format test notebooks-check data-check check

install:
	$(PYTHON) -m pip install -r requirements.txt

install-dev:
	$(PYTHON) -m pip install -r requirements.txt -r requirements-dev.txt

lint:
	ruff check stack_exchange_analysis/src scripts tests

format:
	ruff format stack_exchange_analysis/src scripts tests


test:
	pytest -q

notebooks-check:
	$(PYTHON) scripts/validate_notebooks.py

data-check:
	$(PYTHON) scripts/check_source_data.py

check: lint test notebooks-check data-check
