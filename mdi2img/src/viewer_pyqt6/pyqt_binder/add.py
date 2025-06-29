from PyQt6.QtWidgets import (
    QLabel, QPushButton, QFrame, QGroupBox, QSpinBox, QLineEdit, QTextEdit, QScrollArea,
    QComboBox, QDateEdit, QSplitter, QWidget
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QPixmap


class AddPyQt:
    """ Class for adding GUI elements in PyQt6 """

    def add_label(self, text: str, fg: str, bkg: str, font: tuple = ("Times New Roman", 12)) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(f"color: {fg}; background-color: {bkg};")
        label.setFont(QFont(*font))
        return label

    def add_button(self, text: str, fg: str, bkg: str, command, font: tuple = ("Times New Roman", 12)) -> QPushButton:
        button = QPushButton(text)
        button.setStyleSheet(f"color: {fg}; background-color: {bkg};")
        button.setFont(QFont(*font))
        button.clicked.connect(command)
        return button

    def add_frame(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        return frame

    def add_labelframe(self, title: str, font: tuple = ("Times New Roman", 12)) -> QGroupBox:
        group = QGroupBox(title)
        group.setFont(QFont(*font))
        return group

    def add_spinbox(self, minimum: int, maximum: int, fg: str, bkg: str) -> QSpinBox:
        spin = QSpinBox()
        spin.setMinimum(minimum)
        spin.setMaximum(maximum)
        spin.setStyleSheet(f"color: {fg}; background-color: {bkg};")
        return spin

    def add_entry(self, default_text: str = "", font: tuple = ("Times New Roman", 12)) -> QLineEdit:
        entry = QLineEdit()
        entry.setText(default_text)
        entry.setFont(QFont(*font))
        return entry

    def add_paragraph_field(self, fg: str = "black", bkg: str = "white", font: tuple = ()) -> QTextEdit:
        paragraph = QTextEdit()
        paragraph.setStyleSheet(f"color: {fg}; background-color: {bkg};")
        paragraph.setFont(QFont(*font))
        return paragraph

    def add_dropdown(self, elements: list[str], default_choice: int = 0, fg: str = "#000000", bkg: str = "#FFFFFF", font: tuple = ("Helvetica", 12)) -> QComboBox:
        combo = QComboBox()
        combo.addItems(elements)
        combo.setCurrentIndex(default_choice)
        combo.setStyleSheet(f"color: {fg}; background-color: {bkg};")
        combo.setFont(QFont(*font))
        return combo

    def add_date_field(self, date_pattern: str = "dd/MM/yyyy", fg: str = "black", bkg: str = "white", font: tuple = ("Times New Roman", 12)) -> QDateEdit:
        date_edit = QDateEdit()
        date_edit.setDisplayFormat(date_pattern)
        date_edit.setDate(QDate.currentDate())
        date_edit.setStyleSheet(f"color: {fg}; background-color: {bkg};")
        date_edit.setFont(QFont(*font))
        return date_edit

    def add_splitter(self, orientation: Qt.Orientation = Qt.Orientation.Horizontal) -> QSplitter:
        return QSplitter(orientation)

    def add_image(self, image_path: str) -> QLabel:
        label = QLabel()
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        return label

    def add_scrollbox(self, content_widget: QWidget) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        return scroll

    def add_watermark(self, text: str = "© Created by Henry Letellier", fg: str = "black", bkg: str = "white", font: tuple = ("Times New Roman", 12)) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(f"color: {fg}; background-color: {bkg};")
        label.setFont(QFont(*font))
        return label
