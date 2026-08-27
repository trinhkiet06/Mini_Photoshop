import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import numpy as np
import matplotlib.pyplot as plt
from Processing.histogram import histogram_color


def plot_histogram_color(original: np.ndarray, equalized: np.ndarray):
    _, axes = plt.subplots(2, 2, figsize=(9, 6))

    axes[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Ảnh ban đầu")
    axes[0, 0].axis('off')

    axes[0, 1].imshow(cv2.cvtColor(equalized, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title("Ảnh sau khi cân bằng")
    axes[0, 1].axis('off')

    colors = ('b', 'g', 'r')
    labels = ('Blue', 'Green', 'Red')

    for i, col in enumerate(colors):
        hist_orig = cv2.calcHist([original], [i], None, [256], [0, 256])
        axes[1, 0].plot(hist_orig, color=col, label=labels[i])
        
    axes[1, 0].set_title("Histogram ảnh ban đầu")
    axes[1, 0].set_xlim(0, 255)
    axes[1, 0].legend()

    for i, col in enumerate(colors):
        hist_eq = cv2.calcHist([equalized], [i], None, [256], [0, 256])
        axes[1, 1].plot(hist_eq, color=col, label=labels[i])
    axes[1, 1].set_title("Histogram ảnh sau cân bằng")
    axes[1, 1].set_xlim(0, 255)
    axes[1, 1].legend()

    plt.tight_layout()


def test_image(image_path: str):
    original = cv2.imread(image_path)  # đọc ảnh màu

    if original is None:
        print(f"Không đọc được ảnh: {image_path}")
        return

    equalized = histogram_color(original)

    print(f"Đang test ảnh: {image_path}")
    plot_histogram_color(original, equalized)


if __name__ == "__main__":
    image_paths = ["Data/anh10.png", "Data/anh11.png"]

    for path in image_paths:
        test_image(path)

    plt.show()