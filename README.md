# card-cropper
# Problem
I have been trying to sell my baseball card collection on eBay. The photo-cropping process has been a painful one.
My printer (HP Envy 6055) allows for relatively quick scans. It packages all scans into a folder that I can save.
It would be convenient if I could feed that folder into a script and have code auto-crop them. This would make posting to eBay faster.

# General Work Flow / Pipeline
1. Raw scans are placed into `cards_raw`
* These are full-frame `.jpg` images of the cards

2. Label with LabelImg
* Command: `make label`
* If errors arise, try command: `make patch`

3. Using LabelImg, draw bounding boxes around images 
* Annotations are saved as `.txt` files in `annotations/`

4. Move annotations to training folder
* Copy each `.txt` file from `annotations/` to `dataset/labels/train`
* Copy each `.jpg` file from `cards_raw` to `dataset/images/train`
* Command: `make prep`

5. Validate that all training images have matching labels/annotations
* Command: `make validate`

6. Retrain the model
* Command: `make retrain`
* This fine-tunes your existing YOLOv8 model (`best.pt`) using the updated training set
* The model learns from your newly annotated examples

7. Apply model
* Command: `make predict`
* This uses your trained model to detect cards in `cards_raw/`
* Results are saved to `runs/detect/predict/` with bounding boxes drawn on each image

8. Crop predictions
* Command: `make crop`
* This looks at the latest prediction folder and crops the images for posting