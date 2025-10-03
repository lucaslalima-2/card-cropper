import cv2
import os

IMG_DIR = "cards_raw"
LABEL_DIR = "annotations"
CLASS_NAMES = ["baseball_card", "football_card"]  # match your classes.txt

for filename in os.listdir(IMG_DIR):
	if not filename.endswith(".jpg"):
		continue

	img_path = os.path.join(IMG_DIR, filename)
	label_path = os.path.join(LABEL_DIR, filename.replace(".jpg", ".txt"))

	img = cv2.imread(img_path)
	h, w = img.shape[:2]

	if not os.path.exists(label_path):
		continue

	with open(label_path, "r") as f:
		for line in f:
				cls_id, x, y, bw, bh = map(float, line.strip().split())
				x1 = int((x - bw / 2) * w)
				y1 = int((y - bh / 2) * h)
				x2 = int((x + bw / 2) * w)
				y2 = int((y + bh / 2) * h)

				cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
				cv2.putText(
					img, 
					CLASS_NAMES[int(cls_id)], (x1, y1 - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0),
					2
				)

	cv2.imshow("Preview", img)
	cv2.waitKey(0)