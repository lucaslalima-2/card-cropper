import os
import shutil

CARDS_RAW = "cards_raw"
ANNOTATIONS = "annotations"
IMAGES_TRAIN = "dataset/images/train"
LABELS_TRAIN = "dataset/labels/train"

os.makedirs(IMAGES_TRAIN, exist_ok=True)
os.makedirs(LABELS_TRAIN, exist_ok=True)

added = 0
skipped = 0
missing_labels = 0

for filename in os.listdir(CARDS_RAW):
    if not filename.endswith(".jpg"):
        continue

    image_src = os.path.join(CARDS_RAW, filename)
    image_dst = os.path.join(IMAGES_TRAIN, filename)

    if not os.path.exists(image_dst):
        shutil.copy(image_src, image_dst)
        label_name = filename.replace(".jpg", ".txt")
        label_src = os.path.join(ANNOTATIONS, label_name)
        label_dst = os.path.join(LABELS_TRAIN, label_name)

        if os.path.exists(label_src):
            shutil.copy(label_src, label_dst)
            print(f"✅ Added {filename} and its annotation.")
            added += 1
        else:
            print(f"⚠️  No annotation found for {filename}.")
            missing_labels += 1
    else:
        print(f"⏩ Skipped {filename} (already exists).")
        skipped += 1

print(f"\nSummary:")
print(f"  ✅ Added: {added}")
print(f"  ⏩ Skipped: {skipped}")
print(f"  ⚠️  Missing annotations: {missing_labels}")
