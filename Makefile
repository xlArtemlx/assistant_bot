VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest

.PHONY: venv install run clean

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py

test:
	$(PYTHON) -m pytest -v

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m black .

fix:
	$(PYTHON) -m ruff check . --fix
	$(PYTHON) -m black .

check: lint test

clean:
	rm -rf $(VENV)
	rm -rf build dist *.egg-info