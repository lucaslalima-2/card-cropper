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

  # Contors
  contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  if not contours:
    print("ERROR")
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

  # Find largest countour
  largest = max(contours, key=cv2.contourArea)
  x, y, w, h = cv2.boundingRect(largest)

  # Build result
  cropped = img[y:y+h, x:x+w]
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