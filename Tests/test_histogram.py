import sys
import os

# Thêm thư mục gốc dự án (thư mục cha của file này) vào sys.path
# để Python có thể tìm thấy package "Processing" dù chạy file này từ đâu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Thư viện làm việc và xử lý ảnh
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Processing.histogram import histogram

def plot_histogram(original: np.ndarray, equalized: np.ndarray):

    _, axes = plt.subplots(2, 2, figsize=(8, 6))

    # Hàng 1: ảnh
    axes[0, 0].imshow(original, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title("Ảnh ban đầu")
    axes[0, 0].axis('off')

    axes[0, 1].imshow(equalized, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title("Ảnh sau khi cân bằng")
    axes[0, 1].axis('off')

    # Hàng 2: histogram
    hist_orig, _ = np.histogram(original.flatten(), bins=256, range=(0, 256))
    hist_eq, _ = np.histogram(equalized.flatten(), bins=256, range=(0, 256))

    axes[1, 0].bar(range(256), hist_orig, width=1, color='blue')
    axes[1, 0].set_title("Histogram của ảnh ban đầu")
    axes[1, 0].set_xlim(0, 255)

    axes[1, 1].bar(range(256), hist_eq, width=1, color='blue')
    axes[1, 1].set_title("Histogram của ảnh sau cân bằng")
    axes[1, 1].set_xlim(0, 255)

    plt.tight_layout()

def test_image(image_path: str):
    """
    Đọc ảnh, cân bằng histogram và hiển thị so sánh.
    """
    # Đọc ảnh ở chế độ grayscale
    original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if original is None:
        print(f"Không đọc được ảnh: {image_path}")
        return

    equalized = histogram(original)

    print(f"Đang test ảnh: {image_path}")
    plot_histogram(original, equalized)


if __name__ == "__main__":
    image_paths = ["Data/anh10.png", "Data/anh11.png"]

    for path in image_paths:
        test_image(path)

    plt.show()