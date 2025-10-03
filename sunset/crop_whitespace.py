# First attempt
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