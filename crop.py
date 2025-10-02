# Libraries
import os, sys
from PIL import Image
import numpy as np

def main(indir, outdir):
  # if outdir doesnt exist, make it
  os.makedires(outdir, exist_ok=True)

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