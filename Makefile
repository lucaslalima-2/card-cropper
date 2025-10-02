SCRIPT = crop_cards.py
INPUT_DIR ?= cards_raw
OUTPUT_DIR ?= cards_cropped

setup:
	pip install -r requirements

run:
	python $(SCRIPT) $(INPUT_DIR) $(OUTPUT_DIR)

clean:
	rm -rf $(OUTPUT_DIR)/*