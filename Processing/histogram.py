import numpy as np
import cv2

def equalize_channel(channel: np.ndarray):
    hist, _ = np.histogram(channel.flatten(), bins=256, range=(0, 256))
    cdf = hist.cumsum()
    cdf_normalize = cdf * 255 / cdf[-1]
    gut = np.round(cdf_normalize).astype(np.uint8)
    return gut[channel]


def histogram_color(img_bgr: np.ndarray):
    ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)

    y_eq = equalize_channel(y)

    merged = cv2.merge([y_eq, cr, cb])
    result = cv2.cvtColor(merged, cv2.COLOR_YCrCb2BGR)
    return result