# Libraries
import os, sys, cv2
from PIL import Image
import numpy as np

def remove_background(imagepath):
  # Load image
  img = cv2.imread(imagepath)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Threshold setting
  _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

  # Find largest contour
  contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  if not contours:
    print("ERROR")
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

  # Find largest countour
  largest = max(contours, key=cv2.contourArea)

  # Get minimum area rectangle
  rect = cv2.minAreaRect(largest)
  box = cv2.boxPoints(rect)
  box = np.int32(box)

  # Calculate angle 
  angle = rect[2] 
  if rect[1][0] < rect[1][1]:  # width < height
      angle += 90

  # Find new center of rotated image
  (h, w) = img.shape[:2]
  center = (w // 2, h // 2)

  # Compute rotation matrix
  rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)

  # Compute new bounding dimensions
  cos = np.abs(rot_mat[0, 0])
  sin = np.abs(rot_mat[0, 1])
  new_w = int((h * sin) + (w * cos))
  new_h = int((h * cos) + (w * sin))

  # Adjust rotation matrix to account for translation
  rot_mat[0, 2] += (new_w / 2) - center[0]
  rot_mat[1, 2] += (new_h / 2) - center[1]

  # Rotate entire image
  rotated = cv2.warpAffine(img, rot_mat, (new_w, new_h), flags=cv2.INTER_CUBIC)

  # Recalculate contours on rotated image
  # Use adaptive threshold to handle black borders and variable lighting
  rotated_gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
  rotated_thresh = cv2.adaptiveThreshold(
      rotated_gray, 255,
      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
      cv2.THRESH_BINARY_INV,
      blockSize=71,  # smaller blockSize = more local sensitivity
      C=10           # tweak this to adjust sensitivity
  ) # adaptiveThresh
  rotated_contours, _ = cv2.findContours(rotated_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  if not rotated_contours:
      print("ERROR after rotation")
      return Image.fromarray(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))

  # Crop using largest contour in rotated image
  largest_rotated = max(rotated_contours, key=cv2.contourArea)

  # Get rotated rectangle from largest contour
  rect = cv2.minAreaRect(largest_rotated)
  box = cv2.boxPoints(rect)
  box = np.int32(box)

  # Get bounding box from rotated rectangle
  x, y, w, h = cv2.boundingRect(box)

  # Padding
  pad = 10
  x_pad = max(x - pad, 0)
  y_pad = max(y - pad, 0)
  x2_pad = min(x + w + pad, rotated.shape[1])
  y2_pad = min(y + h + pad, rotated.shape[0])

  cropped = rotated[y_pad:y2_pad, x_pad:x2_pad]

  # Ensure portrait orientation
  if cropped.shape[1] > cropped.shape[0]:  # width > height
    cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)

  return Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

def main(indir, outdir):
  # if outdir doesnt exist, make it
  os.makedirs(outdir, exist_ok=True)

  # Finds all jpgs and sends to crop function
  for root, dirs, files in os.walk(indir):
    for file in files:
      if file.lower().endswith(".jpg"):
        cardpath = os.path.join(root, file) # Find card path
        outpath = os.path.join(outdir, file) # crop the card, and store result
        result = remove_background(cardpath) # crop
        result.save(outpath) # put result in outpath
  return

if __name__ == "__main__":
  main(sys.argv[1], sys.argv[2])