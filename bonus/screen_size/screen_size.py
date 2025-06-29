##
# EPITECH PROJECT, 2024
# MDI2IMG
# File description:
# screen_size.py
##

import sys
from typing import Dict

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QRect, Qt


@staticmethod
def get_current_host_screen_dimensions(parent_window: QMainWindow) -> Dict[str, int]:
    """
    Create a temporary hidden tool window to determine the screen geometry on which
    the application is currently running, then destroy the window.

    Args:
        parent_window (QMainWindow): The parent window used to anchor the screen lookup.

    Returns:
        dict: {"width": width, "height": height, "left": left, "top": top}
    """
    temp_window = QMainWindow(parent_window, Qt.WindowType.Tool)
    temp_window.show()
    temp_window.hide()
    parent_window.repaint()  # make sure events are processed
    parent_window.app.processEvents()  # if needed for parent updates

    screen_geometry: QRect = temp_window.screen().geometry()

    temp_window.close()
    temp_window.deleteLater()

    return {
        "width": screen_geometry.width(),
        "height": screen_geometry.height(),
        "left": screen_geometry.left(),
        "top": screen_geometry.top(),
    }


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create a top-level main window (no subclassing)
    main_window = QMainWindow()
    main_window.setWindowTitle("Main Window")
    main_window.resize(800, 600)
    main_window.show()

    # Optional: attach app to main_window for access inside helper
    main_window.app = app

    dims = get_current_host_screen_dimensions(main_window)
    print("Screen dimensions:", dims)

    # Start event loop
    sys.exit(app.exec())
