"""
Retrains the model building off last best.pt
"""

import os
import subprocess

# Path to your training runs
RUNS_DIR = "runs/detect"
DATA_YAML = "data.yaml"
EPOCHS = 20
IMG_SIZE = 640

# Find latest train folder
train_folders = [f for f in os.listdir(RUNS_DIR) if f.startswith("train")]
train_folders.sort(key=lambda x: os.path.getmtime(os.path.join(RUNS_DIR, x)), reverse=True)

if not train_folders:
    raise FileNotFoundError("No previous training folders found in runs/detect")

latest_train = train_folders[0]
model_path = os.path.join(RUNS_DIR, latest_train, "weights", "best.pt")

# Run YOLOv8 training
subprocess.run([
    "yolo",
    "task=detect",
    "mode=train",
    f"model={model_path}",
    f"data={DATA_YAML}",
    f"epochs={EPOCHS}",
    f"imgsz={IMG_SIZE}"
])
