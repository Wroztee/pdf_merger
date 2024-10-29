from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QSizePolicy, QScrollArea, QMainWindow
from PySide6.QtCore import QSize, Qt
import pdf2image as pdf2img
from PyPDF2 import PdfReader

from main import merge_pdf, select_pdf_paths, select_out_path, get_page_count

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Merger")
        self.setGeometry(100, 100, 700, 400)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.setCentralWidget(self.scroll_area)
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        self.load_button = QPushButton("Load PDFs")
        self.load_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.load_button.clicked.connect(self.load_pdf_files)
        self.generate_button = QPushButton("Generate PDF")
        self.generate_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.generate_button.clicked.connect(self.generate_pdf)

        top_button_layout = QHBoxLayout()
        top_button_layout.addWidget(self.load_button)
        top_button_layout.addWidget(self.generate_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(top_button_layout)
        self.main_layout.addStretch()

        self.scroll_widget.setLayout(self.main_layout)

        self.item_widgets = []


    def add_pdf(self, path : str, page_count : int):
        pdf_widget = ItemRow(path, page_count)
        self.main_layout.insertWidget(len(self.item_widgets), pdf_widget)
        self.item_widgets.append(pdf_widget)


    def load_pdf_files(self):
        pdf_paths = select_pdf_paths()
        for path in pdf_paths:
            page_count = get_page_count(path)
            self.add_pdf(path, page_count)


    def generate_pdf(self):
        out_path = select_out_path()

        paths = []
        pages = []

        for widget in self.item_widgets:
            paths.append(widget.path)
            pages.append((widget.start_page_spin_box.value() - 1, widget.end_page_spin_box.value()))

        merge_pdf(paths, out_path, pages)
        print(f"PDF created at {out_path}")


class ItemRow(QWidget):
    def __init__(self, path : str, page_count : int):
        super().__init__()

        self.path = path
        self.page_count = page_count

        reader = PdfReader(path)

        self.image = pdf2img.convert_from_path(path, dpi=20, first_page=0, last_page=1)[0]
        self.image_label = QLabel(self)
        self.image_label.setPixmap(self.image.toqpixmap().scaled(100, 150, Qt.KeepAspectRatio))
        self.image_label.setScaledContents(True)

        self.path_label = QLabel(f".../{path.split("/")[-1]}")
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


    def end_page_changed(self, value):
        self.start_page_spin_box.setRange(1, value)


    def move_item_up(self):
        parent = self.parentWidget()
        current_idx = parent.item_widgets.index(self)
        if (current_idx == 0):
            return
        
        parent.item_widgets.pop(current_idx)
        parent.item_widgets.insert(current_idx - 1, self)

        parent.main_layout.removeWidget(self)
        parent.main_layout.insertWidget(current_idx - 1, self)


    def move_item_down(self):
        parent = self.parentWidget()
        current_idx = parent.item_widgets.index(self)
        if (current_idx == len(parent.item_widgets) - 1):
            return
        
        parent.item_widgets.pop(current_idx)
        parent.item_widgets.insert(current_idx + 1, self)

        parent.main_layout.removeWidget(self)
        parent.main_layout.insertWidget(current_idx + 1, self)


    def remove_item(self):
        parent = self.parentWidget()
        parent.item_widgets.remove(self)
        parent.main_layout.removeWidget(self)
        self.deleteLater()


if __name__ == "__main__":
    app = QApplication()

    window = MainWindow()
    window.show()

    app.exec()