from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QImage, QMouseEvent, QPixmap, QPainter, QPalette, QColor
from PySide6.QtCore import Signal
from utils import repaint_image


class LoadPDFButton(QLabel):
    def __init__(self, image_path: str = "icons/add_pdf.png"):
        super().__init__()

        image = QImage(image_path)
        color = QColor(127, 127, 127, 255)
        self.setPixmap(QPixmap(repaint_image(image, color, QPainter.CompositionMode.CompositionMode_SourceIn)))
        self.setScaledContents(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


