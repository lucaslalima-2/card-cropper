SCRIPT = crop.py
INPUT_DIR ?= cards_raw
OUTPUT_DIR ?= cards_cropped
VENV=.venv
PYTHON = .venv/bin/python

venv:
	python3 -m venv $(VENV)

setup: venv
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

run:
	$(PYTHON) $(SCRIPT) $(INPUT_DIR) $(OUTPUT_DIR)

clean:
	rm -rf $(OUTPUT_DIR)/*