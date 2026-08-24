import sys
import os

# Thêm thư mục gốc dự án (thư mục cha của file này) vào sys.path
# để Python có thể tìm thấy package "Processing" dù chạy file này từ đâu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from GUI.panels import ControlPanel, DisplayPanel


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
        self.control_panel = ControlPanel()
        self.control_panel.btn_open.clicked.connect(self.load_image)
        self.control_panel.btn_save.clicked.connect(self.save_image)
        self.control_panel.btn_reset.clicked.connect(self.reset_image)

        # KHU VỰC HIỂN THỊ
        self.display_panel = DisplayPanel()

        # GHÉP GIAO DIỆN
        main_layout.addWidget(self.control_panel, 1)
        main_layout.addWidget(self.display_panel, 3)

    # MỞ ẢNH
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn Ảnh", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:
            self.original_image = file_path
            self.processed_image = file_path

            self.display_image(file_path, self.display_panel.lbl_orig)
            self.display_image(file_path, self.display_panel.lbl_proc)

    # LƯU ẢNH
    def save_image(self):
        if self.processed_image is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Lưu Ảnh", "", "PNG (*.png);;JPG (*.jpg)")

        if file_path:
            pixmap = self.display_panel.lbl_proc.pixmap()

            if pixmap:
                pixmap.save(file_path)

    # ĐẶT LẠI
    def reset_image(self):
        if self.original_image is not None:
            self.control_panel.slider_bright.setValue(0)
            self.control_panel.slider_contrast.setValue(10)
            self.control_panel.slider_blur.setValue(1)
            self.control_panel.btn_hist.setChecked(False)
            self.processed_image = self.original_image
            self.display_image(self.original_image, self.display_panel.lbl_proc)

    # HIỂN THỊ ẢNH
    def display_image(self, file_path, label):
        pixmap = QPixmap(file_path)

        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                label.width(), label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)


# CHẠY CHƯƠNG TRÌNH
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiniPhotoshop()
    window.show()
    sys.exit(app.exec_())