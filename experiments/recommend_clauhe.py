"""
File thử nghiệm: So sánh Histogram Equalization toàn cục (đã dùng trong app)
với CLAHE (đề xuất cải tiến) — không phải chức năng chính thức của app,
chỉ phục vụ mục đích phân tích, minh họa trong báo cáo.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from Processing.histogram import histogram_color  # tái sử dụng hàm chính thức

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "experiments")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def histogram_color_clahe(img_bgr, clip_limit=2.0, tile_size=(8, 8)):
    """Chỉ dùng để SO SÁNH minh họa, không tích hợp vào GUI chính."""
    ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    y_eq = clahe.apply(y)
    merged = cv2.merge([y_eq, cr, cb])
    return cv2.cvtColor(merged, cv2.COLOR_YCrCb2BGR)


def compute_metrics(original, processed):
    """Tính các chỉ số đánh giá: std, entropy, noise, psnr, ssim"""
    gray_orig = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    gray_proc = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)

    std_val = gray_proc.std()

    hist, _ = np.histogram(gray_proc.flatten(), bins=256, range=(0, 256))
    hist = hist[hist > 0] / hist.sum()
    entropy_val = -np.sum(hist * np.log2(hist))

    smoothed = cv2.GaussianBlur(gray_proc, (5, 5), 0)
    noise_val = np.std(gray_proc.astype(np.float32) - smoothed.astype(np.float32))

    psnr_val = psnr(gray_orig, gray_proc)
    ssim_val = ssim(gray_orig, gray_proc)

    return {
        "std": std_val,
        "entropy": entropy_val,
        "noise": noise_val,
        "psnr": psnr_val,
        "ssim": ssim_val,
    }


def compare_methods(image_path):
    """
    Gộp chung 1 hình, chia 2 hàng:
    - Hàng trên (1x3): Ảnh gốc - Global HE - CLAHE
    - Hàng dưới (1x1): Biểu đồ cột so sánh các chỉ số
    """
    original = cv2.imread(image_path)
    eq_global = histogram_color(original)
    eq_clahe = histogram_color_clahe(original)

    metrics_global = compute_metrics(original, eq_global)
    metrics_clahe = compute_metrics(original, eq_clahe)

    print(f"{'Chỉ số':<12}{'Global HE':<15}{'CLAHE':<15}")
    for key in metrics_global:
        print(f"{key:<12}{metrics_global[key]:<15.3f}{metrics_clahe[key]:<15.3f}")

    # Bố cục 2 hàng: hàng trên chia 3 cột con cho ảnh, hàng dưới 1 biểu đồ
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.2], hspace=0.35)

    # Hàng trên: 3 ảnh
    gs_top = gs[0].subgridspec(1, 3)
    images = [original, eq_global, eq_clahe]
    titles = ["Ảnh gốc", "Global HE", "CLAHE"]
    for i, (img, title) in enumerate(zip(images, titles)):
        ax = fig.add_subplot(gs_top[0, i])
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax.set_title(title)
        ax.axis("off")

    # Hàng dưới: biểu đồ cột so sánh chỉ số
    ax_bar = fig.add_subplot(gs[1])
    labels = list(metrics_global.keys())
    global_vals = list(metrics_global.values())
    clahe_vals = list(metrics_clahe.values())

    x = np.arange(len(labels))
    width = 0.35
    ax_bar.bar(x - width / 2, global_vals, width, label="Global HE", color="orange")
    ax_bar.bar(x + width / 2, clahe_vals, width, label="CLAHE", color="green")
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels)
    ax_bar.set_title("So sánh chỉ số: Global HE vs CLAHE")
    ax_bar.legend()

    plt.savefig(os.path.join(OUTPUT_DIR, "clahe_vs_global_full.png"))
    plt.show()

    return metrics_global, metrics_clahe


if __name__ == "__main__":
    image_path = os.path.join(BASE_DIR, "..", "Data", "anh11.png")
    compare_methods(image_path)