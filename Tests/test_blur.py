import sys
import os

# Thêm thư mục gốc dự án vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import matplotlib.pyplot as plt
from Processing.blur import blur_color

# data ảnh cần test
target_images = ["anh8.png"]

# thuật toán test blur
def show_blur_test(img, size_values, sigma_values):
    plt.figure(figsize=(15, 8))

    for i, size in enumerate(size_values):
        for j, sigma in enumerate(sigma_values):
            result = blur_color(img, size=size, sigma=sigma)

            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

            index = i * len(sigma_values) + j + 1
            plt.subplot(len(size_values), len(sigma_values), index)

            plt.imshow(result_rgb)
            plt.title(f"(Size = {size}, Sigma = {sigma})")
            plt.axis("off")

    plt.tight_layout()
    plt.show()


size_values = [3, 5, 9, 13, 21]
sigma_values = [0.5, 1.0, 2.0, 3.0, 5.0]

for filename in target_images:
    path = os.path.join("Data", filename)

    img = cv2.imread(path)
    if img is None:
        continue
    print(f"Testing: {path}...")
    show_blur_test(img, size_values, sigma_values)