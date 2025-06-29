import os
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon


class SetPyQt:
    """Class for setting properties on PyQt6 widgets."""

    def set_transparency(self, window: QWidget, alpha: float) -> None:
        """Set the transparency of the window (0.0 to 1.0)."""
        if alpha < 0:
            alpha = abs(alpha)
        if alpha > 1:
            alpha = 1.0
        window.setWindowOpacity(alpha)

    def set_window_title_bar_visibility(self, window: QWidget, visible: bool = True) -> None:
        """Set title bar visibility (removes decorations if not visible)."""
        window.setWindowFlag(Qt.WindowType.FramelessWindowHint, not visible)
        window.show()  # Needed to apply the flag change

    def set_title(self, window: QWidget, title: str) -> None:
        """Set the title of the window."""
        window.setWindowTitle(title)

    def set_window_size(self, window: QWidget, width: int, height: int, posx: int = None, posy: int = None) -> None:
        """Set the size and optionally the position of the window."""
        window.resize(width, height)
        if posx is not None and posy is not None:
            window.move(posx, posy)

    def set_min_window_size(self, window: QWidget, width: int, height: int) -> None:
        """Set minimum window size."""
        window.setMinimumSize(width, height)

    def set_max_window_size(self, window: QWidget, width: int, height: int) -> None:
        """Set maximum window size."""
        window.setMaximumSize(width, height)

    def set_window_position(self, window: QWidget, posx: int, posy: int) -> None:
        """Set position of the window."""
        window.move(posx, posy)

    def set_window_background_colour(self, window: QWidget, colour: str) -> None:
        """Set background color of the window using stylesheet."""
        window.setStyleSheet(f"background-color: {colour};")

    def set_icon(self, window: QWidget, icon_path: str) -> None:
        """Set the window icon."""
        if os.path.exists(icon_path) and os.path.isfile(icon_path):
            window.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Icon path '{icon_path}' does not exist.")

    def set_window_always_on_top(self, window: QWidget, always_on_top: bool = True) -> None:
        """Set window to stay on top."""
        window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, always_on_top)
        window.show()

    def set_window_visible(self, window: QWidget, visible: bool = True) -> None:
        """Set window visibility."""
        if visible:
            window.show()
        else:
            window.hide()

    def set_interaction_possible(self, window: QWidget, interaction_enabled: bool = True) -> None:
        """Enable or disable window interaction."""
        window.setEnabled(interaction_enabled)
