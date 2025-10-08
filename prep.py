import os, argparse
import shutil

# Argparser
parser = argparse.ArgumentParser(description="Moves annotations images (*.jpg) & labels (*.txt) to one of two destination folders.")
parser.add_argument('--input_folder', help="Scanned images (usually ./cards_raw)")
parser.add_argument('--training', action="store_true", help='Move to training folder')
parser.add_argument('--evaluating', action="store_true", help='Move to evaluation folder')
args = parser.parse_args()

# Variables
if args.training:
	dest_img = "./dataset/images/train"
	dest_lab = "./dataset/labels/train"
elif args.evaluating:
	dest_img = "./dataset/images/val"
	dest_lab = "./dataset/labels/val"
else:
	print("(E) prep.py -> Please pick destination folder: [--testing, --evaluation]")
	exit()

# Catch
if args.training and args.evaulating:
	print("(E) prep.py -> User can only pick one destination folder: [--testing, --evaluation]")
	exit()

ANNOTATIONS = "annotations"
os.makedirs(dest_img, exist_ok=True)
os.makedirs(dest_lab, exist_ok=True)

added = 0
skipped = 0
missing_labels = 0

for filename in os.listdir(args.input_folder):
	if not filename.endswith(".jpg"):
		continue

	image = os.path.join(args.input_folder, filename)
	label = os.path.join(ANNOTATIONS, filename.replace(".jpg", ".txt"))
	matching_img = os.path.join(dest_img, filename)
	matching_lab = os.path.join(dest_lab, filename.replace(".jpg", ".txt"))

	if not os.path.exists(matching_img):
		shutil.move(image, matching_img)
		print(f"Coppying: {image} -> {matching_img}")

		if not os.path.exists(matching_lab): # Moving
			shutil.move(label, matching_lab)
			print(f"✅ Added {filename} and its annotation.")
			added += 1
		else: # Already present
			print(f"⚠️ Annotation already exists for {filename}.")
			missing_labels += 1
	else: # JPG already exists
		print(f"⏩ Skipped {filename} (already exists).")
		skipped += 1

print(f"\nSummary:")
print(f"  ✅ Added: {added}")
print(f"  ⏩ Skipped: {skipped}")
print(f"  ⚠️  Missing annotations: {missing_labels}")
