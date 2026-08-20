import sys
import os

# Thêm thư mục gốc dự án (thư mục cha của file này) vào sys.path
# để Python có thể tìm thấy package "Processing" dù chạy file này từ đâu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Thư viện làm việc và xử lý ảnh
import cv2
import matplotlib.pyplot as plt
from Processing.brightness_contrast import brightness_constract

# data ảnh cần test
target_images = ["anh5.png"]

# thuật toán test độ sáng và độ tương phản
def show_brightness_constract_test(img, brightness_values_beta, contrast_values_beta):
    plt.figure(figsize=(15, 8))

    for i, beta in enumerate(brightness_values_beta):
        for j, alpha in enumerate(contrast_values_beta):
            result = brightness_constract(img, alpha = alpha, beta = beta)

            result_rpg = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

            index = i * len(brightness_values_beta) + j + 1
            plt.subplot(len(brightness_values_beta), len(contrast_values_beta), index)

            plt.imshow(result_rpg)
            plt.title(f"(Alpha = {alpha}, Beta = {beta})")
            plt.axis("off")

    plt.tight_layout()
    plt.show()

brightness_values_beta = [-50, -30, 0, 30, 50]
contrast_values_beta =[0.5, 0.75, 1.0, 1.25, 1.5]

for filename in target_images:
    path = os.path.join("Data", filename)

    img = cv2.imread(path)
    if img is None:
        continue
    print(f"Testing: {path}...")
    show_brightness_constract_test(img, brightness_values_beta, contrast_values_beta)