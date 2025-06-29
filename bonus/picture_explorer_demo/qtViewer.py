import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ImageViewer(QWidget):
    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths
        self.current_index = 0

        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Widgets
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.prev_button = QPushButton("Previous")
        self.open_button = QPushButton("Open in System Viewer")
        self.next_button = QPushButton("Next")

        self.prev_button.clicked.connect(self.show_prev_image)
        self.next_button.clicked.connect(self.show_next_image)
        self.open_button.clicked.connect(self.open_in_viewer)

        # Layouts
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.prev_button)
        btn_layout.addWidget(self.open_button)
        btn_layout.addWidget(self.next_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        self.update_image()

    def update_image(self):
        if not self.image_paths:
            self.image_label.setText("No images found.")
            return

        path = self.image_paths[self.current_index]
        if not os.path.exists(path):
            self.image_label.setText(f"Image not found: {path}")
            return

        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.image_label.setText(f"Failed to load image: {path}")
        else:
            scaled_pixmap = pixmap.scaled(self.image_label.size(
            ), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        self.update_image()

    def show_next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index +
                                  1) % len(self.image_paths)
            self.update_image()

    def show_prev_image(self):
        if self.image_paths:
            self.current_index = (self.current_index -
                                  1) % len(self.image_paths)
            self.update_image()

    def open_in_viewer(self):
        if self.image_paths:
            path = self.image_paths[self.current_index]
            if os.name == 'nt':
                os.startfile(path)
            elif sys.platform == 'darwin':
                os.system(f"open '{path}'")
            else:
                os.system(f"xdg-open '{path}'")


def select_images():
    """Open a file dialog to select images and display them in the ImageViewer."""
    app = QApplication(sys.argv)
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")

    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        viewer = ImageViewer(selected_files)
        viewer.show()
        sys.exit(app.exec())


if __name__ == '__main__':
    select_images()
