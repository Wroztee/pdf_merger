from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QSizePolicy
from PySide6.QtCore import QSize, QMimeData, Qt
from PySide6.QtGui import QDrag, QPixmap, QMouseEvent, QPalette, QColor, QImage, QPainter
import pdf2image as pdf2img
from PyPDF2 import PdfReader

from utils import add_image_transparency


class PdfItemWidget(QWidget):
    def __init__(self, path : str, page_count : int):
        super().__init__()

        self.preview_images = {}

        self.path = path
        self.page_count = page_count

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Mid)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        reader = PdfReader(path)

        image = pdf2img.convert_from_path(path, dpi=20, first_page=1, last_page=1)[0].toqpixmap().scaled(100, 150, Qt.KeepAspectRatio)
        self.preview_images[1] = image
        self.image_label = QLabel(self)
        self.image_label.setPixmap(image)
        self.image_label.setScaledContents(True)
        self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.path_label = QLabel(f".../{path.split('/')[-1]}")
        self.path_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.title_label = QLabel()
        if "/Title" in reader.metadata and reader.metadata["/Title"] != "":
            self.title = reader.metadata["/Title"]
            self.title_label.setText("Title: " + self.title)

        self.creator_label = QLabel()
        if "/Creator" in reader.metadata and reader.metadata["/Creator"] != "":
            self.creator = reader.metadata["/Creator"]
            self.creator_label.setText("Creator: " + self.creator)

        self.producer_label = QLabel()
        if "/Producer" in reader.metadata and reader.metadata["/Producer"] != "":
            self.producer = reader.metadata["/Producer"]
            self.producer_label.setText("Producer: " + self.producer)

        self.start_page_spin_box = QSpinBox()
        self.start_page_spin_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.start_page_spin_box.setRange(1, page_count)
        self.start_page_spin_box.setValue(1)
        self.start_page_spin_box.valueChanged.connect(self.start_page_changed)

        self.end_page_spin_box = QSpinBox()
        self.end_page_spin_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.end_page_spin_box.setRange(1, page_count)
        self.end_page_spin_box.setValue(page_count)
        self.end_page_spin_box.valueChanged.connect(self.end_page_changed)

        self.up_button = QPushButton("↑")
        self.up_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.up_button.clicked.connect(self.move_item_up)

        self.down_button = QPushButton("↓")
        self.down_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.down_button.clicked.connect(self.move_item_down)

        self.remove_button = QPushButton("Remove")
        self.remove_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.remove_button.clicked.connect(self.remove_item)


        self.main_layout = QHBoxLayout()

        self.main_layout.addWidget(self.image_label, 1)

        self.info_layout = QVBoxLayout()
        self.info_layout.addWidget(self.path_label)
        self.info_layout.addWidget(self.title_label)
        self.info_layout.addWidget(self.creator_label)
        self.info_layout.addWidget(self.producer_label)
        self.info_layout.addStretch()
        self.main_layout.addLayout(self.info_layout, 3)

        self.page_range_layout = QVBoxLayout()
        self.page_range_layout.addStretch()
        self.page_range_layout.addWidget(self.start_page_spin_box)
        self.page_range_layout.addWidget(self.end_page_spin_box)
        self.main_layout.addLayout(self.page_range_layout, 1)
        self.page_range_layout.addStretch()

        self.move_page_layout = QVBoxLayout()
        self.move_page_layout.addStretch()
        self.move_page_layout.addWidget(self.up_button)
        self.move_page_layout.addWidget(self.down_button)
        self.main_layout.addLayout(self.move_page_layout, 1)
        self.move_page_layout.addStretch()

        self.main_layout.addWidget(self.remove_button, 1)

        self.setLayout(self.main_layout)


    def start_page_changed(self, value):
        self.end_page_spin_box.setRange(value, self.page_count)
        if value in self.preview_images:
            self.image_label.setPixmap(self.preview_images[value])
            return
        image = pdf2img.convert_from_path(self.path, dpi=20, first_page=value, last_page=value)[0].toqpixmap().scaled(
            100, 150, Qt.KeepAspectRatio)
        self.preview_images[value] = image
        self.image_label.setPixmap(image)


    def end_page_changed(self, value):
        self.start_page_spin_box.setRange(1, value)


    def move_item_up(self):
        parent = self.parentWidget()
        current_idx = parent.item_widgets.index(self)
        parent.move_item_widget(current_idx, current_idx - 1)


    def move_item_down(self):
        parent = self.parentWidget()
        current_idx = parent.item_widgets.index(self)
        parent.move_item_widget(current_idx, current_idx + 1)


    def remove_item(self):
        parent = self.parentWidget()
        parent.item_widgets.remove(self)
        parent.layout().removeWidget(self)
        self.deleteLater()


    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.image_label.size())
            self.image_label.render(pixmap)
            drag.setPixmap(add_image_transparency(pixmap, 127))

            drag.exec(Qt.DropAction.MoveAction)

