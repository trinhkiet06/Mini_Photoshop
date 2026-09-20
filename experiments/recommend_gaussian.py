"""
File thử nghiệm: So sánh Mean Blur (Average) và Gaussian Blur
cùng kernel size — không phải chức năng chính thức của app,
chỉ phục vụ mục đích phân tích, minh họa trong báo cáo.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from Processing.blur import blur_color  # chỉ hỗ trợ Gaussian

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "experiments")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def mean_blur_color(img_bgr, size=9):
    """Mean Blur - chưa có trong Processing/blur.py nên viết tạm ở đây để so sánh"""
    return cv2.blur(img_bgr, (size, size))


def compute_metrics(original, processed):
    gray_orig = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    gray_proc = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)

    sharpness_val = cv2.Laplacian(gray_proc, cv2.CV_64F).var()

    edges_orig = cv2.Canny(gray_orig, 100, 200)
    edges_proc = cv2.Canny(gray_proc, 100, 200)
    edge_density_val = np.sum(edges_proc > 0) / max(np.sum(edges_orig > 0), 1)

    noise_orig = np.std(gray_orig.astype(np.float32) - cv2.GaussianBlur(gray_orig, (5, 5), 0).astype(np.float32))
    noise_proc = np.std(gray_proc.astype(np.float32) - cv2.GaussianBlur(gray_proc, (5, 5), 0).astype(np.float32))
    noise_reduction_val = noise_orig - noise_proc

    psnr_val = psnr(gray_orig, gray_proc)
    ssim_val = ssim(gray_orig, gray_proc)

    return {
        "sharpness": sharpness_val,
        "edge_density": edge_density_val,
        "noise_reduction": noise_reduction_val,
        "psnr": psnr_val,
        "ssim": ssim_val,
    }


def compare_methods(image_path, size=9, sigma=2.0):
    original = cv2.imread(image_path)
    mean_result = mean_blur_color(original, size=size)
    gaussian_result = blur_color(original, size=size, sigma=sigma)

    metrics_mean = compute_metrics(original, mean_result)
    metrics_gaussian = compute_metrics(original, gaussian_result)

    print(f"{'Chỉ số':<18}{'Mean Blur':<15}{'Gaussian Blur':<15}")
    for key in metrics_mean:
        print(f"{key:<18}{metrics_mean[key]:<15.3f}{metrics_gaussian[key]:<15.3f}")

    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.2], hspace=0.35)

    gs_top = gs[0].subgridspec(1, 3)
    images = [original, mean_result, gaussian_result]
    titles = ["Ảnh gốc", f"Mean Blur (size={size})", f"Gaussian Blur (size={size}, σ={sigma})"]
    for i, (img, title) in enumerate(zip(images, titles)):
        ax = fig.add_subplot(gs_top[0, i])
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax.set_title(title)
        ax.axis("off")

    ax_bar = fig.add_subplot(gs[1])
    labels = list(metrics_mean.keys())
    mean_vals = list(metrics_mean.values())
    gaussian_vals = list(metrics_gaussian.values())

    x = np.arange(len(labels))
    width = 0.35
    ax_bar.bar(x - width / 2, mean_vals, width, label="Mean Blur", color="steelblue")
    ax_bar.bar(x + width / 2, gaussian_vals, width, label="Gaussian Blur", color="salmon")
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels)
    ax_bar.set_title("So sánh chỉ số: Mean Blur vs Gaussian Blur")
    ax_bar.legend()

    plt.savefig(os.path.join(OUTPUT_DIR, "mean_vs_gaussian_full.png"))
    plt.show()

    return metrics_mean, metrics_gaussian


if __name__ == "__main__":
    image_path = os.path.join(BASE_DIR, "..", "Data", "anh9.png")
    compare_methods(image_path, size=9, sigma=2.0)