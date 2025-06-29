import os
import random
import string
from typing import Union
from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QApplication
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class UnsortedPyQt:
    """ Miscellaneous utilities not tied to a single widget type """

    def gen_random_name(self, length: int = 10) -> str:
        """ Generate a random string name """
        return ''.join(random.choices(string.ascii_letters, k=length))

    def init_plain_window(self, root_window: Union[QWidget, None] = None) -> QWidget:
        """ Return a new top-level QWidget """
        if isinstance(root_window, QWidget):
            return QWidget(parent=root_window)
        return QWidget()  # PyQt does not distinguish root/child in the same way

    def init_window(self, window: QWidget, title: str, bkg: str, width: int, height: int, position_x: int, position_y: int, fullscreen: bool, resizable: bool) -> None:
        """ Initialize window properties """
        window.setGeometry(position_x, position_y, width, height)
        window.setWindowTitle(title)
        window.setStyleSheet(f"background-color: {bkg};")
        window.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, resizable)
        if fullscreen:
            window.showFullScreen()
        else:
            window.showNormal()

    def load_image(self, image_path: str, width: int = 10, height: int = 10) -> dict[str, any]:
        """ Load and scale an image """
        result = {}
        if not os.path.exists(image_path) or not os.path.isfile(image_path):
            result["err_message"] = "Image path is not valid or not provided"
            return result
        if height <= 0 or width <= 0:
            result["err_message"] = "Image width and height must be greater than 0"
            return result
        try:
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(width, height)
            result["img"] = pixmap
        except Exception as error:
            result["err_message"] = str(error)
        return result

    def create_text_variable(self, default_text: str) -> str:
        """ PyQt6 doesn't use StringVar — return plain string """
        return default_text

    def clear_entry_content(self, entry: QLineEdit) -> None:
        """ Clear all content in a line edit """
        entry.clear()

    def update_entry_content(self, entry: QLineEdit, position: int, new_text: str) -> None:
        """ Insert text at position in a QLineEdit """
        current = entry.text()
        updated = current[:position] + new_text + current[position:]
        entry.setText(updated)

    def enter_fullscreen(self, window: QWidget, fullscreen: bool) -> None:
        """ Toggle fullscreen mode """
        if fullscreen:
            window.showFullScreen()
        else:
            window.showNormal()

    def allow_resizing(self, window: QWidget, allow: bool = True) -> None:
        """ Allow or prevent resizing (sets fixed size if False) """
        if not allow:
            window.setFixedSize(window.width(), window.height())
        else:
            window.setMinimumSize(0, 0)
            window.setMaximumSize(16777215, 16777215)  # max PyQt6 size

    def maintain_on_top(self, window: QWidget, always_on_top: bool) -> None:
        """ Keep window always on top """
        window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, always_on_top)
        window.show()

    def free_loaded_image(self, image_pointer: QPixmap) -> None:
        """ Explicitly delete pixmap """
        try:
            del image_pointer
        except Exception:
            pass
