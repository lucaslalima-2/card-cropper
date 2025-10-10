"""
Used to crop predictions made by model
"""
# Libaries
import os, cv2, yaml
from PIL import Image
import numpy as np

# Functions
from src.remove_background import remove_background
from src.find_latest_predict_dir import find_latest_predict_dir

# Variables
PREDICTION_DIR = find_latest_predict_dir()
LABELS_DIR = os.path.join(PREDICTION_DIR, "labels")
OUTPUT_DIR = "cards_cropped"

# Makes outdir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sets class name
with open("data.yaml", "r") as f:
    class_names = yaml.safe_load(f)["names"]

# Finds label
for label_file in os.listdir(LABELS_DIR):
	image_name = label_file.replace(".txt", ".jpg")
	image_path = os.path.join("cards_raw", image_name)
	label_path = os.path.join(LABELS_DIR, label_file)

	# Loads image
	img = cv2.imread(image_path)
	h, w = img.shape[:2] # gets h,w of image

	# Crops image for each annotation in label file
	with open(label_path, "r") as f:
		for i, line in enumerate(f): #0 0.490294 0.573423 0.391437 0.354059
			cls_id, x_center, y_center, box_w, box_h = map(float, line.strip().split())
			x1 = int((x_center - box_w / 2) * w)
			y1 = int((y_center - box_h / 2) * h)
			x2 = int((x_center + box_w / 2) * w)
			y2 = int((y_center + box_h / 2) * h)

			# Crops image based on annotation coords
			crop = img[y1:y2, x1:x2]
			temp_path = "temp_crop.jpg"
			cv2.imwrite(temp_path, crop)

			# Removes background
			cleaned = remove_background(temp_path)
			class_name = class_names[int(cls_id)]
			cropped_img = f"{label_file.replace('.txt','')}_{class_name}_{i}.jpg"
			cleaned.save(os.path.join(OUTPUT_DIR, cropped_img))

# Removes temp img
if os.path.exists("temp_crop.jpg"):
	os.remove("temp_crop.jpg")