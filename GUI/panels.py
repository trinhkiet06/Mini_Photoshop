from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QSlider, QVBoxLayout, QHBoxLayout,
    QGridLayout, QGroupBox, QFrame
)
from PyQt5.QtCore import Qt

# STYLESHEET HIỆN ĐẠI & TINH TẾ (CATPPUCCIN MOCHA / MODERN DARK)
STYLE_SHEET = """
QMainWindow {
    background-color: #11111b;
    color: #cdd6f4;
}

QWidget {
    background-color: #11111b;
    color: #cdd6f4;
    font-family: 'Segoe UI', Roboto, sans-serif;
}

QGroupBox {
    color: #89b4fa;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid #313244;
    border-radius: 10px;
    margin-top: 15px;
    padding: 15px 10px 10px 10px;
    background-color: #181825;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 10px;
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 6px;
    color: #89b4fa;
}

QLabel {
    color: #a6adc8;
    font-size: 13px;
}

QPushButton {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 9px 16px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #313244;
    border-color: #89b4fa;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #89b4fa;
    color: #11111b;
}

QPushButton:checked {
    background-color: #89b4fa;
    color: #11111b;
    font-weight: bold;
    border: none;
}

QSlider::groove:horizontal {
    border: none;
    height: 6px;
    background: #313244;
    border-radius: 3px;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #89b4fa,
        stop:1 #cba6f7
    );
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #cdd6f4;
    border: 2px solid #89b4fa;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background: #ffffff;
    border-color: #cba6f7;
}

.image-card {
    border: 1px solid #313244;
    border-radius: 12px;
    background-color: #181825;
    color: #6c7086;
    font-size: 13px;
    padding: 5px;
}

.image-title {
    font-size: 14px;
    font-weight: 600;
    color: #cdd6f4;
    margin-bottom: 4px;
}
"""


# PANEL ĐIỀU KHIỂN BÊN TRÁI
class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(STYLE_SHEET)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(12)
        layout.setContentsMargins(10, 10, 10, 10)

        # 1. NHÓM TẬP TIN
        file_box = QGroupBox("Tập Tin")
        file_layout = QVBoxLayout()
        file_layout.setSpacing(8)

        self.btn_open = QPushButton("📁  Mở Ảnh (Open)")
        self.btn_save = QPushButton("💾  Lưu Ảnh (Save)")
        self.btn_reset = QPushButton("🔄  Đặt Lại (Reset)")

        file_layout.addWidget(self.btn_open)
        file_layout.addWidget(self.btn_save)
        file_layout.addWidget(self.btn_reset)
        file_box.setLayout(file_layout)
        layout.addWidget(file_box)

        # 2. NHÓM ĐIỀU CHỈNH THÔNG SỐ
        adj_box = QGroupBox("Điều Chỉnh Thông Số")
        adj_layout = QVBoxLayout()
        adj_layout.setSpacing(12)

        # Brightness
        bright_header = QHBoxLayout()
        bright_header.addWidget(QLabel("Độ Sáng:"))
        self.lbl_bright_val = QLabel("0")
        self.lbl_bright_val.setAlignment(Qt.AlignRight)
        self.lbl_bright_val.setStyleSheet("color: #89b4fa; font-weight: bold;")
        bright_header.addWidget(self.lbl_bright_val)

        self.slider_bright = QSlider(Qt.Horizontal)
        self.slider_bright.setRange(-100, 100)
        self.slider_bright.setValue(0)
        self.slider_bright.valueChanged.connect(
            lambda v: self.lbl_bright_val.setText(str(v))
        )

        adj_layout.addLayout(bright_header)
        adj_layout.addWidget(self.slider_bright)

        # Contrast
        contrast_header = QHBoxLayout()
        contrast_header.addWidget(QLabel("Độ Tương Phản:"))
        self.lbl_contrast_val = QLabel("1.0")
        self.lbl_contrast_val.setAlignment(Qt.AlignRight)
        self.lbl_contrast_val.setStyleSheet("color: #89b4fa; font-weight: bold;")
        contrast_header.addWidget(self.lbl_contrast_val)

        self.slider_contrast = QSlider(Qt.Horizontal)
        self.slider_contrast.setRange(0, 30)
        self.slider_contrast.setValue(10)
        self.slider_contrast.valueChanged.connect(
            lambda v: self.lbl_contrast_val.setText(f"{v/10.0:.1f}")
        )

        adj_layout.addLayout(contrast_header)
        adj_layout.addWidget(self.slider_contrast)

        # --- 1. Blur Kernel Size ---
        blur_size_header = QHBoxLayout()
        blur_size_header.addWidget(QLabel("Độ Mờ - Kích Thước (Size):"))
        self.lbl_blur_size_val = QLabel("1")
        self.lbl_blur_size_val.setAlignment(Qt.AlignRight)
        self.lbl_blur_size_val.setStyleSheet("color: #89b4fa; font-weight: bold;")
        blur_size_header.addWidget(self.lbl_blur_size_val)

        self.slider_blur_size = QSlider(Qt.Horizontal)
        self.slider_blur_size.setRange(1, 25) # Size từ 1 đến 25
        self.slider_blur_size.setValue(1)
        self.slider_blur_size.valueChanged.connect(
            lambda v: self.lbl_blur_size_val.setText(str(v if v % 2 != 0 else v + 1))
        )

        adj_layout.addLayout(blur_size_header)
        adj_layout.addWidget(self.slider_blur_size)

        # --- 2. Blur Sigma ---
        blur_sigma_header = QHBoxLayout()
        blur_sigma_header.addWidget(QLabel("Độ Mờ - Độ Lan Tỏa (Sigma):"))
        self.lbl_blur_sigma_val = QLabel("0.0")
        self.lbl_blur_sigma_val.setAlignment(Qt.AlignRight)
        self.lbl_blur_sigma_val.setStyleSheet("color: #89b4fa; font-weight: bold;")
        blur_sigma_header.addWidget(self.lbl_blur_sigma_val)

        self.slider_blur_sigma = QSlider(Qt.Horizontal)
        self.slider_blur_sigma.setRange(0, 100) # Quy đổi 0 đến 100 thành 0.0 đến 10.0
        self.slider_blur_sigma.setValue(0)
        self.slider_blur_sigma.valueChanged.connect(
            lambda v: self.lbl_blur_sigma_val.setText(f"{v / 10.0:.1f}")
        )

        adj_layout.addLayout(blur_sigma_header)
        adj_layout.addWidget(self.slider_blur_sigma)
        
        # Histogram Button
        self.btn_hist = QPushButton("📊  Cân Bằng Histogram")
        self.btn_hist.setCheckable(True)
        adj_layout.addWidget(self.btn_hist)

        adj_box.setLayout(adj_layout)
        layout.addWidget(adj_box)

        layout.addStretch()


# PANEL HIỂN THỊ BÊN PHẢI
class DisplayPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(STYLE_SHEET)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(15)
        grid.setContentsMargins(10, 10, 10, 10)

        # Tiêu đề
        title_orig = QLabel("Ảnh Gốc")
        title_orig.setProperty("class", "image-title")
        title_orig.setAlignment(Qt.AlignCenter)

        title_proc = QLabel("Ảnh Sau Khi Xử Lý")
        title_proc.setProperty("class", "image-title")
        title_proc.setAlignment(Qt.AlignCenter)

        title_hist = QLabel("Biểu Đồ Histogram")
        title_hist.setProperty("class", "image-title")
        title_hist.setAlignment(Qt.AlignCenter)

        # Label hiển thị
        self.lbl_orig = QLabel("Chưa mở ảnh")
        self.lbl_orig.setAlignment(Qt.AlignCenter)
        self.lbl_orig.setMinimumSize(380, 280)
        self.lbl_orig.setProperty("class", "image-card")

        self.lbl_proc = QLabel("Chưa có kết quả")
        self.lbl_proc.setAlignment(Qt.AlignCenter)
        self.lbl_proc.setMinimumSize(380, 280)
        self.lbl_proc.setProperty("class", "image-card")

        self.histogram_label = QLabel("Histogram sẽ hiển thị ở đây")
        self.histogram_label.setAlignment(Qt.AlignCenter)
        self.histogram_label.setMinimumSize(780, 140)
        self.histogram_label.setProperty("class", "image-card")

        # Đưa vào Grid
        grid.addWidget(title_orig, 0, 0)
        grid.addWidget(title_proc, 0, 1)
        grid.addWidget(self.lbl_orig, 1, 0)
        grid.addWidget(self.lbl_proc, 1, 1)
        grid.addWidget(title_hist, 2, 0, 1, 2)
        grid.addWidget(self.histogram_label, 3, 0, 1, 2)

        # Tỷ lệ co dãn các dòng/cột
        grid.setRowStretch(1, 3)
        grid.setRowStretch(3, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
