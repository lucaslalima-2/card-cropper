"""
Wraps YOLO bounding-box prediction command so that you can walk through
sub directories
"""

# Libraries
import os, subprocess

INPUT_ROOT = "annotations"
MODELS_DIR = "./runs/detect/"

# Find latest train folder
train_folders = [f for f in os.listdir(RUNS_DIR) if f.startswith("train")]
train_folders.sort(key=lambda x: os.path.getmtime(os.path.join(RUNS_DIR, x)), reverse=True)
latest_train_folder = train_folders[0]
MODEL_PATH =  os.path.join(RUNS_DIR, latest_train, "weights", "best.pt")

# Loop through all subfolders and files
for root, _, files in os.walk(INPUT_ROOT):
	for file in files:
		if file.endswith(".jpg") or file.endswith(".png"):
				image_path = os.path.join(root, file)

				# Run YOLOv8 predict command
				subprocess.run([
						"yolo",
						"task=detect",
						"mode=predict",
						f"model={MODEL_PATH}",
						f"source={image_path}",
						"save_txt=True",
						"save_conf=False",
						"save=False"
				])