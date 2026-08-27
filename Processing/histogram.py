import numpy as np

def histogram(gray:np.ndarray):
    hist,_ = np.histogram(gray.flatten(),bins=256,range=(0,256))

    cdf = hist.cumsum()

    cdf_normalize = cdf*255 / cdf[-1]
    gut = np.round(cdf_normalize).astype(np.uint8)

    return gut[gray]

