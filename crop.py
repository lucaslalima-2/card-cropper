# Libraries
import os, sys
from PIL import Image
import numpy as np

def crop_whitespace(jpg):
  img = Image.open(jpg).convert("RGB")
  np_img = np.array(img)

  # Convert to grayscale
  gray = np.mean(np_img, axis=2)

  # Eliminate scan light-bleeding
  h, w = gray.shape
  edge_margin = 0.20

  gray_central = gray [
    int(h * edge_margin):int(h * (1-edge_margin)),
    int(w * edge_margin):int(w * (1-edge_margin))
  ]

  # Mask
  mask = gray_central < 240
  
  # Show mask
  mask_img = Image.fromarray((mask*255).astype(np.uint8))
  mask_img.show()

  coords = np.argwhere(mask)
  print(coords)
  if coords.size == 0:
    print(f"No content found in {jpg}")
    return img
  
  # Adjusts coords back to full image space
  y0, x0 = coords.min(axis=0)
  y1, x1 = coords.max(axis=0) + 1 # includes edge
  y0 += int(h * edge_margin)
  y1 += int(h * edge_margin)
  x0 += int(w * edge_margin)
  x1 += int(w * edge_margin)

  cropped = img.crop((x0, y0, x1, y1))

  return cropped

def main(indir, outdir):
  # if outdir doesnt exist, make it
  os.makedirs(outdir, exist_ok=True)

  # Finds all jpgs and sends to crop function
  for root, dirs, files in os.walk(indir):
    for file in files:
      if file.lower().endswith(".jpg"):
        cardpath = os.path.join(root, file) # Find card path
        outpath = os.path.join(outdir, file) # crop the card, and store result
        result = crop_whitespace(cardpath) # crop
        result.save(outpath) # put result in outpath
  return

if __name__ == "__main__":
  main(sys.argv[1], sys.argv[2])