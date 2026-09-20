import sys
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Processing.blur import blur_color
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

from GUI.panels1 import ControlPanel, DisplayPanel, STYLE_SHEET

# Giả sử các hàm xử lý thuật toán của bạn nằm trong package Processing
# Ví dụ: from Processing.enhancement import adjust_brightness_contrast, apply_blur, equalize_histogram


class MiniPhotoshop(QMainWindow):
    def __init__(self):
        super().__init__()
        # Áp dụng giao diện tối cho toàn bộ cửa sổ
        self.setStyleSheet(STYLE_SHEET)

        self.original_cv_img = None
        self.processed_cv_img = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Mini Photoshop - Chủ đề 3")
        self.setGeometry(100, 100, 1200, 700)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        # PANEL ĐIỀU KHIỂN
        self.control_panel = ControlPanel()
        self.control_panel.btn_open.clicked.connect(self.load_image)
        self.control_panel.btn_save.clicked.connect(self.save_image)
        self.control_panel.btn_reset.clicked.connect(self.reset_image)

        # KẾT NỐI SỰ KIỆN CÁC THANH SLIDER VÀ BUTTON VỚI THUẬT TOÁN XỬ LÝ
        self.control_panel.slider_bright.valueChanged.connect(self.apply_processing)
        self.control_panel.slider_contrast.valueChanged.connect(self.apply_processing)
        self.control_panel.slider_blur_size.valueChanged.connect(self.apply_processing)
        self.control_panel.slider_blur_sigma.valueChanged.connect(self.apply_processing)
        self.control_panel.btn_hist.clicked.connect(self.apply_processing)

         # KHU VỰC HIỂN THỊ
        self.display_panel = DisplayPanel()

        # GHÉP GIAO DIỆN
        main_layout.addWidget(self.control_panel, 1)
        main_layout.addWidget(self.display_panel, 3)

    # CHUYỂN ĐỔI TỪ OPENCV MAT (NUMPY ARRAY) SANG QPIXMAP ĐỂ HIỂN THỊ
    def cv2_to_qpixmap(self, cv_img):
        if cv_img is None:
            return QPixmap()
        
        if len(cv_img.shape) == 3:
            h, w, ch = cv_img.shape
            bytes_per_line = ch * w
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            q_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        else:
            h, w = cv_img.shape
            bytes_per_line = w
            q_img = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
            
        return QPixmap.fromImage(q_img)

    # HIỂN THỊ QPIXMAP LÊN LABEL VỚI TỶ LỆ CO DÃN
    def render_pixmap_to_label(self, pixmap, label):
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                label.width(), label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            label.setPixmap(scaled_pixmap)

    # MỞ ẢNH
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn Ảnh", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:
            self.original_cv_img = cv2.imread(file_path)
            if self.original_cv_img is not None:
                self.processed_cv_img = self.original_cv_img.copy()
                pix_orig = self.cv2_to_qpixmap(self.original_cv_img)
                self.render_pixmap_to_label(pix_orig, self.display_panel.lbl_orig)
                self.apply_processing()

    # PIPELINE ÁP DỤNG CÁC THUẬT TOÁN XỬ LÝ ẢNH
    def apply_processing(self):
        if self.original_cv_img is None:
            return

        brightness = self.control_panel.slider_bright.value()      
        contrast = self.control_panel.slider_contrast.value() / 10.0

        blur_size_val = self.control_panel.slider_blur_size.value()
        blur_sigma_val = self.control_panel.slider_blur_sigma.value() / 10.0

        is_hist = self.control_panel.btn_hist.isChecked()

        img = self.original_cv_img.copy()
        # 1. Điều chỉnh độ sáng / tương phản
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
        # 2. Xử lý Blur khi Size > 1
        if blur_size_val > 1:
            ksize = blur_size_val if blur_size_val % 2 != 0 else blur_size_val + 1
            img = blur_color(img, size=ksize, sigma=blur_sigma_val)
        # 3. Cân bằng Histogram
        if is_hist:
            if len(img.shape) == 3:
                ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
                ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
                img = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
            else:
                img = cv2.equalizeHist(img)
        # 4. Hiển thị lại kết quả
        self.processed_cv_img = img
        pix_proc = self.cv2_to_qpixmap(self.processed_cv_img)
        self.render_pixmap_to_label(pix_proc, self.display_panel.lbl_proc)
        self.update_histogram_display(self.processed_cv_img)

    # VẼ VÀ HIỂN THỊ HISTOGRAM LÊN LABEL HISTOGRAM
    def update_histogram_display(self, img):
        plt.figure(figsize=(6, 2), dpi=100)
        plt.style.use('dark_background')

        if len(img.shape) == 3:
            colors = ('b', 'g', 'r')
            for i, col in enumerate(colors):
                hist = cv2.calcHist([img], [i], None, [256], [0, 256])
                plt.plot(hist, color=col, linewidth=1)
        else:
            hist = cv2.calcHist([img], [0], None, [256], [0, 256])
            plt.plot(hist, color='white', linewidth=1)

        plt.xlim([0, 256])
        plt.axis('off') 
        plt.tight_layout(pad=0)

        # Lưu đồ thị ra buffer trong bộ nhớ
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        plt.close()
        buf.seek(0)

        # Load buffer lên QPixmap
        qimg = QImage.fromData(buf.getvalue())
        pix_hist = QPixmap.fromImage(qimg)
        self.render_pixmap_to_label(pix_hist, self.display_panel.histogram_label)

    # LƯU ẢNH
    def save_image(self):
        if self.processed_cv_img is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Lưu Ảnh", "", "PNG (*.png);;JPG (*.jpg)"
        )

        if file_path:
            cv2.imwrite(file_path, self.processed_cv_img)

    # ĐẶT LẠI
    def reset_image(self):
        if self.original_cv_img is not None:
            # Block signals tạm thời để tránh gọi apply_processing liên tục
            self.control_panel.slider_bright.blockSignals(True)
            self.control_panel.slider_contrast.blockSignals(True)
            self.control_panel.slider_blur.blockSignals(True)

            self.control_panel.slider_bright.setValue(0)
            self.control_panel.slider_contrast.setValue(10)
            self.control_panel.slider_blur.setValue(1)
            self.control_panel.btn_hist.setChecked(False)

            self.control_panel.slider_bright.blockSignals(False)
            self.control_panel.slider_contrast.blockSignals(False)
            self.control_panel.slider_blur.blockSignals(False)

            # Chạy lại xử lý với thông số mặc định
            self.apply_processing()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiniPhotoshop()
    window.show()
    sys.exit(app.exec_())
