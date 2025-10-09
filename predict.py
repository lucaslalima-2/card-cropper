"""
Wraps YOLO bounding-box prediction command so that you can walk through
sub directories
"""

# Libraries
import os, subprocess

RUNS_DIR = "./runs/detect/"
IMAGE_DIR = "./cards_raw/"

# Find latest training model
train_folders = [f for f in os.listdir(RUNS_DIR) if f.startswith("train")]
train_folders.sort(key=lambda x: os.path.getmtime(os.path.join(RUNS_DIR, x)), reverse=True)

latest_train_folder = train_folders[0]
MODEL_PATH =  os.path.join(RUNS_DIR, latest_train_folder, "weights", "best.pt")

# === 
# AVOIDING THIS BC IT CREATED A NEW PREDICT FOLDER FOR EACH IMAGE
# ===
# Loop through all subfolders and files
# for root, _, files in os.walk(IMAGE_DIR):
# 	for file in files:
# 		if file.endswith(".jpg") or file.endswith(".png"):
# 				image_path = os.path.join(root, file)

# 				# Run YOLOv8 predict command
# 				subprocess.run([
# 						"yolo",
# 						"task=detect",
# 						"mode=predict",
# 						f"model={MODEL_PATH}",
# 						f"source={image_path}",
# 						"save_txt=True",
# 						"save_conf=False",
# 						"save=False"
# 				])

# Requires all images to be pulled out of subdirs in ./cards_raw
subprocess.run([
	"yolo",
	"task=detect",
	"mode=predict",
	f"model={MODEL_PATH}",
	f"source={IMAGE_DIR}",
	"save_txt=True",
	"save_conf=False",
	"save=False"
])