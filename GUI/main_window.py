import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QPushButton, QSlider, QVBoxLayout, QHBoxLayout,
    QFileDialog, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class MiniPhotoshop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.processed_image = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Mini Photoshop - Chủ đề 3")
        self.setGeometry(100, 100, 1200, 700)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # PANEL ĐIỀU KHIỂN

        control_panel = QVBoxLayout()

        #FILE 
        file_box = QGroupBox("File")
        file_layout = QVBoxLayout()

        btn_open = QPushButton("Mở Ảnh")
        btn_save = QPushButton("Lưu Kết Quả")
        btn_reset = QPushButton("Đặt Lại")

        btn_open.clicked.connect(self.load_image)
        btn_save.clicked.connect(self.save_image)
        btn_reset.clicked.connect(self.reset_image)

        file_layout.addWidget(btn_open)
        file_layout.addWidget(btn_save)
        file_layout.addWidget(btn_reset)

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

        # KHU VỰC HIỂN THỊ
        display_layout = QGridLayout()

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
        self.lbl_proc.setStyleSheet("border: 1px solid black; background-color: #f0f0f0;")

        # Histogram
        self.histogram_label = QLabel("Histogram")
        self.histogram_label.setAlignment(Qt.AlignCenter)
        self.histogram_label.setMinimumSize(800, 150)
        self.histogram_label.setStyleSheet("border: 1px solid black; background-color: #f0f0f0;")
        
        # Đưa các thành phần vào giao diện
        display_layout.addWidget(title_original, 0, 0)
        display_layout.addWidget(title_processed, 0, 1)

        display_layout.addWidget(self.lbl_orig, 1, 0)
        display_layout.addWidget(self.lbl_proc, 1, 1)

        display_layout.addWidget(
            QLabel("Histogram"),2, 0, 1, 2,Qt.AlignCenter)

        display_layout.addWidget(self.histogram_label,3, 0, 1, 2)

        # GHÉP GIAO DIỆN
        main_layout.addLayout(control_panel, 1)
        main_layout.addLayout(display_layout, 3)

    # MỞ ẢNH
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,"Chọn Ảnh","","Image Files (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:
            self.original_image = file_path
            self.processed_image = file_path

            self.display_image(file_path,self.lbl_orig)
            self.display_image(file_path,self.lbl_proc)

    # LƯU ẢNH
    def save_image(self):
        if self.processed_image is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,"Lưu Ảnh","","PNG (*.png);;JPG (*.jpg)")

        if file_path:
            pixmap = self.lbl_proc.pixmap()

            if pixmap:
                pixmap.save(file_path)

    # ĐẶT LẠI
    def reset_image(self):
        if self.original_image is not None:
            self.slider_bright.setValue(0)
            self.slider_contrast.setValue(10)
            self.slider_blur.setValue(1)
            self.btn_hist.setChecked(False)
            self.processed_image = self.original_image
            self.display_image(self.original_image,self.lbl_proc)

    # HIỂN THỊ ẢNH
    def display_image(self, file_path, label):
        pixmap = QPixmap(file_path)

        if not pixmap.isNull():
            pixmap = pixmap.scaled(label.width(),label.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
            label.setPixmap(pixmap)

# CHẠY CHƯƠNG TRÌNH
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiniPhotoshop()
    window.show()
    sys.exit(app.exec_())
