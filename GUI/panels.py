import os
import sys
# Thêm thư mục gốc dự án (thư mục cha của file này) vào sys.path
# để Python có thể tìm thấy package "Processing" dù chạy file này từ đâu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QSlider,
    QVBoxLayout, QGridLayout, QGroupBox
)
from PyQt5.QtCore import Qt


class ControlPanel(QWidget):
    """Panel bên trái: các nút File và thanh trượt điều chỉnh thông số."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        control_panel = QVBoxLayout()
        self.setLayout(control_panel)

        # FILE
        file_box = QGroupBox("File")
        file_layout = QVBoxLayout()

        self.btn_open = QPushButton("Mở Ảnh")
        self.btn_save = QPushButton("Lưu Kết Quả")
        self.btn_reset = QPushButton("Đặt Lại")

        file_layout.addWidget(self.btn_open)
        file_layout.addWidget(self.btn_save)
        file_layout.addWidget(self.btn_reset)

        file_box.setLayout(file_layout)
        control_panel.addWidget(file_box)

        # ĐIỀU CHỈNH
        adj_box = QGroupBox("Điều Chỉnh Thông Số")
        adj_layout = QVBoxLayout()

        # Brightness
        adj_layout.addWidget(QLabel("Độ Sáng (Brightness):"))
        self.slider_bright = QSlider(Qt.Horizontal)
        self.slider_bright.setRange(-100, 100)
        self.slider_bright.setValue(0)
        adj_layout.addWidget(self.slider_bright)

        # Contrast
        adj_layout.addWidget(QLabel("Độ Tương Phản (Contrast):"))
        self.slider_contrast = QSlider(Qt.Horizontal)
        self.slider_contrast.setRange(0, 30)
        self.slider_contrast.setValue(10)
        adj_layout.addWidget(self.slider_contrast)

        # Blur
        adj_layout.addWidget(QLabel("Độ Mờ (Blur):"))
        self.slider_blur = QSlider(Qt.Horizontal)
        self.slider_blur.setRange(1, 25)
        self.slider_blur.setValue(1)
        adj_layout.addWidget(self.slider_blur)

        # Histogram
        self.btn_hist = QPushButton("Cân Bằng Histogram")
        self.btn_hist.setCheckable(True)
        adj_layout.addWidget(self.btn_hist)

        adj_box.setLayout(adj_layout)
        control_panel.addWidget(adj_box)

        control_panel.addStretch()


class DisplayPanel(QWidget):
    """Panel bên phải: hiển thị ảnh gốc, ảnh đã xử lý và histogram."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        display_layout = QGridLayout()
        self.setLayout(display_layout)

        # Tiêu đề ảnh gốc
        title_original = QLabel("Ảnh Gốc")
        title_original.setAlignment(Qt.AlignCenter)

        # Tiêu đề ảnh xử lý
        title_processed = QLabel("Ảnh Sau Khi Xử Lý")
        title_processed.setAlignment(Qt.AlignCenter)

        # Label ảnh gốc
        self.lbl_orig = QLabel("Chưa chọn ảnh")
        self.lbl_orig.setAlignment(Qt.AlignCenter)
        self.lbl_orig.setMinimumSize(400, 300)
        self.lbl_orig.setStyleSheet(
            "border: 1px solid black; background-color: #f0f0f0;"
        )

        # Label ảnh xử lý
        self.lbl_proc = QLabel("Chưa có kết quả")
        self.lbl_proc.setAlignment(Qt.AlignCenter)
        self.lbl_proc.setMinimumSize(400, 300)
        self.lbl_proc.setStyleSheet(
            "border: 1px solid black; background-color: #f0f0f0;"
        )

        # Histogram
        self.histogram_label = QLabel("Histogram")
        self.histogram_label.setAlignment(Qt.AlignCenter)
        self.histogram_label.setMinimumSize(800, 150)
        self.histogram_label.setStyleSheet(
            "border: 1px solid black; background-color: #f0f0f0;"
        )

        # Đưa các thành phần vào giao diện
        display_layout.addWidget(title_original, 0, 0)
        display_layout.addWidget(title_processed, 0, 1)

        display_layout.addWidget(self.lbl_orig, 1, 0)
        display_layout.addWidget(self.lbl_proc, 1, 1)

        display_layout.addWidget(
            QLabel("Histogram"), 2, 0, 1, 2, Qt.AlignCenter)

        display_layout.addWidget(self.histogram_label, 3, 0, 1, 2)