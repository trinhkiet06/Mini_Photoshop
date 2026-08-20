import numpy as np

# thuật toán brightness_contrast
def brightness_constract(img, alpha = 1, beta = 0) -> list:
  result = img.astype(np.float32) * alpha + beta
  result = np.clip(result, 0, 255)
  return result.astype(np.uint8)