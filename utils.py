from PySide6.QtGui import QImage, QPixmap, QPainter, QColor



def add_image_transparency(image: QImage | QPixmap, alpha: int) -> QImage | QPixmap:
    return repaint_image(image, QColor(0, 0, 0, alpha), QPainter.CompositionMode.CompositionMode_DestinationIn)


def repaint_image(image: QImage | QPixmap, color: QColor | tuple, composition_mode: QPainter.CompositionMode) -> QImage | QPixmap:
    input_type = type(image)

    if input_type == QPixmap:
        image = image.toImage()

    if type(color) == tuple:
        color = QColor(*color)
    
    painter = QPainter()
    painter.begin(image)
    painter.setCompositionMode(composition_mode)
    painter.fillRect(image.rect(), color)
    painter.end()

    if input_type == QPixmap:
        return QPixmap(image)
    return image
