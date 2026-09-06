import cv2

def blur_color(img_bgr, size=9, sigma=2.0):
    return cv2.GaussianBlur(img_bgr, (size, size), sigma)