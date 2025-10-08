SCRIPT = crop.py
INPUT_DIR ?= cards_raw
VENV=.venv
PYTHON = .venv/bin/python
MODEL = runs/detect/train/weights/best.pt

crop:
	$(PYTHON) crop_predictions.py 

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
	yolo task=detect mode=predict model=$(MODEL) source=$(INPUT_DIR) save_txt=True save_conf=False save=False

prep-train:
	$(PYTHON) prep.py --input_folder cards_raw --testing

prep-eval:
	$(PYTHON) prep.py --input_folder cards_raw --evaluating

preview:
	$(PYTHON) preview_label_annotations.py

retrain:
	yolo task=detect mode=train model=runs/detect/train/weights/best.pt data=data.yaml epochs=20 imgsz=640

validate:
	$(PYTHON) validate_dataset.py

clean:
	rm -rf $(OUTPUT_DIR)/*