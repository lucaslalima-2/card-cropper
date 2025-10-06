"""
Run after sorting images (.jpgs) and description files (.txts)
"""

import os

def check_alignment(image_dir, label_dir):
    images = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]
    labels = [f for f in os.listdir(label_dir) if f.endswith(".txt")]

    missing_labels = []
    for img in images:
        label = img.replace(".jpg", ".txt")
        if label not in labels:
            missing_labels.append(img)

    if missing_labels:
        print("Images missing labels:")
        for img in missing_labels:
            print(f"  - {img}")
    else:
        print("✅ All images have matching labels.")

check_alignment("dataset/images/train", "dataset/labels/train")
check_alignment("dataset/images/val", "dataset/labels/val")