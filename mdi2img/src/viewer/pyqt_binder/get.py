from PyQt6.QtWidgets import QLineEdit, QWidget, QFileDialog, QApplication
from PyQt6.QtGui import QPixmap


class GetPyQt:
    """Class to retrieve information from PyQt6 GUI elements."""

    def get_entry_content(self, entry: QLineEdit) -> str:
        """Get the text content from a QLineEdit."""
        return entry.text()

    def get_window_width(self, window: QWidget) -> int:
        """Get the width of the window."""
        return window.width()

    def get_window_height(self, window: QWidget) -> int:
        """Get the height of the window."""
        return window.height()

    def get_window_position_x(self, window: QWidget) -> int:
        """Get the x position of the window."""
        return window.x()

    def get_window_position_y(self, window: QWidget) -> int:
        """Get the y position of the window."""
        return window.y()

    def get_window_position(self, window: QWidget) -> tuple[int, int]:
        """Get the (x, y) position of the window."""
        return window.x(), window.y()

    def get_window_geometry(self, window: QWidget) -> str:
        """Get the geometry string of the window."""
        geo = window.geometry()
        return f"{geo.width()}x{geo.height()}+{geo.x()}+{geo.y()}"

    def get_window_size(self, window: QWidget) -> tuple[int, int]:
        """Get the size (width, height) of the window."""
        return window.width(), window.height()

    def get_window_title(self, window: QWidget) -> str:
        """Get the window title."""
        return window.windowTitle()

    def get_filepath(self, window: QWidget, filetypes: list[tuple[str, str]] = [('Text files', '*.txt'), ('All files', '*.*')]) -> str:
        """Open a file picker and return selected file path."""
        filter_str = ";;".join([f"{desc} ({ext})" for desc, ext in filetypes])
        filename, _ = QFileDialog.getOpenFileName(
            window, "Open File", "", filter_str)
        return filename

    def get_folderpath(self, window: QWidget, initial_directory: str = "") -> str:
        """Open a folder picker and return selected folder path."""
        return QFileDialog.getExistingDirectory(window, "Select Folder", initial_directory)

    def get_current_host_screen_dimensions(self, window: QWidget) -> dict:
        """Get current screen dimensions."""
        screen = window.screen().geometry()
        return {
            "width": screen.width(),
            "height": screen.height(),
            "left": screen.left(),
            "top": screen.top()
        }

    def get_image_dimensions(self, image: QPixmap) -> dict[str, int]:
        """Get image dimensions."""
        return {
            "width": image.width(),
            "height": image.height()
        }
