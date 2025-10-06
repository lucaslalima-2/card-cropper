SCRIPT = crop.py
INPUT_DIR ?= ./dataset/images/train
# OUTPUT_DIR ?= 
VENV=.venv
PYTHON = .venv/bin/python

venv:
	python3.11 -m venv $(VENV)

setup: venv
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	mkdir -p annotations

label:
	$(VENV)/bin/labelImg $(INPUT_DIR) classes.txt annotations

preview:
	$(PYTHON) preview_label_annotations.py

patch:
	patch .venv/lib/python3.11/site-packages/labelImg/labelImg.py < docs/labelimg.patch
	patch .venv/lib/python3.11/site-packages/libs/canvas.py < docs/canvas.patch

validate:
	$(PYTHON) validate_dataset.py
clean:
	rm -rf $(OUTPUT_DIR)/*