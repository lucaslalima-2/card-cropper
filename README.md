# card-cropper
# Problem
I have been trying to sell my baseball card collection on eBay. The photo-cropping process has been a painful one.
My printer (HP Envy 6055) allows for relatively quick scans. It packages all scans into a folder that I can save.
It would be convenient if I could feed that folder into a script and have code auto-crop them. This would make posting to eBay faster.

# General Work Flow / Pipeline
1. Raw scans are placed into `cards_raw`
* These are full-frame `.jpg` images of the cards.

2. Label Bounding Boxes with LabelImg
* If errors arise, try command: `make patch`
* For more training, move new images to dataset/images/train and load that with LabelImg > Open Dir.
* Confirm that LabelImg > Change Save Dir points to dataset/labels/train. By default, annotations are saved as `.txt` files in `annotations/`. We don't want this.
* Used the bounding box button on the bottom-left of the GUI to drag-create labels.
* Shortcut (hotkey): W
* Command: `make label`

3. [If desired / Until model is strong] Move validation images to `dataset/images/val` & connected label `.txt` files to `dataset/labels/val`
* We need validation images that are unique to `dataset/images/train` and `dataset/labels/train` to prevent overfitting (poor model decisions).
* Command: `make prep-eval` or `make prep-train`

4. Validate that all training images and validation images have matching labels (`.txt` files)
* Command: `make validate`

5. Retrain the model
* This fine-tunes your existing YOLOv8 model (`best.pt`) using the updated training set.
* The model learns from your newly annotated examples.
* Command: `make retrain`

6. See model predictions on trained data
* Command: `make preview`

7. Apply model
* This uses your trained model to detect cards in `dataset/images/val` or `cards_raw/`.
* Bounding-box results are saved to `runs/detect/predict*/`.
* To save bounding-boxes with images, update final command in `predict.py`.
* These would need to be set true: `"save_conf=False"` & `"save=False"`.
* Command: `make predict-train` or `make preview-raw`

8. Crop predictions
* This looks at the latest prediction folder and crops the images for posting.
* Command: `make crop`

# Metrics to look at when training your model
* Loss (especially box_loss, cls_loss, dfl_loss). These measure how far off your predictions are from the ground truth.
* Smaller is better — ideally decreasing over time

* `mAP@0.5` and `mAP@0.5:0.95`
* These measure how well your model is detecting objects. Larger is better — ideally increasing over time.
* `mAP@0.5`: easier threshold (IoU ≥ 0.5)
* `mAP@0.5:0.95`: stricter, averaged across thresholds