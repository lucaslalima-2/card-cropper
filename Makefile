SCRIPT = crop.py
INPUT_DIR ?= cards_raw
VENV=.venv
PYTHON = .venv/bin/python
MODEL = runs/detect/train/weights/best.pt

crop:
	$(PYTHON) crop.py 

venv:
	python3.11 -m venv $(VENV)

setup: venv
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

label:
	mkdir -p annotations
	$(VENV)/bin/labelImg $(INPUT_DIR) ./annotations/classes.txt annotations

patch:
	patch .venv/lib/python3.11/site-packages/labelImg/labelImg.py < docs/labelimg.patch
	patch .venv/lib/python3.11/site-packages/libs/canvas.py < docs/canvas.patch

predict:
	$(PYTHON) predict.py

prep-train:
	$(PYTHON) prep.py --input_folder cards_raw --training

prep-eval:
	$(PYTHON) prep.py --input_folder cards_raw --evaluating

preview-train:
	$(PYTHON) preview.py --target train

preview-raw:
	$(PYTHON) preview.py --target raw

retrain:
	$(PYTHON) retrain.py

validate:
	$(PYTHON) validate.py

clean:
	rm -rf $(OUTPUT_DIR)/*