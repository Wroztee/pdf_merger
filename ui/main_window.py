from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QScrollArea, QMainWindow
from PySide6.QtGui import QResizeEvent, QPalette

from pdf_utils import merge_pdf, select_pdf_paths, select_out_path, get_page_count
from ui.central_widget import CentralScrollArea
from ui.item_widget import PdfItemWidget
from ui.load_button import LoadPDFButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Merger")
        self.setGeometry(100, 100, 700, 400)

        self.main_layout = QVBoxLayout()

        self.scroll_area = CentralScrollArea()
        self.scroll_widget = self.scroll_area.widget()
        self.scroll_widget.main_window = self
        self.setCentralWidget(self.scroll_area)

        self.load_widget = QWidget()
        self.load_widget.setAutoFillBackground(True)
        self.load_widget.setBackgroundRole(QPalette.Mid)
        self.load_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.load_button = LoadPDFButton()
        self.load_button.mousePressEvent = lambda event: self.load_pdf_files()
        self.load_widget_layout = QHBoxLayout()
        self.load_widget_layout.addWidget(self.load_button)
        self.load_widget_layout.addStretch()
        self.load_widget.setLayout(self.load_widget_layout)

        self.generate_button = QPushButton("Generate PDF", self)
        self.generate_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.generate_button.clicked.connect(self.generate_pdf)
        self.generate_button.setFixedSize(95, 25)

        #top_button_layout = QHBoxLayout()
        #top_button_layout.addWidget(self.load_button)
        #top_button_layout.addWidget(self.generate_button)

        self.main_layout.addWidget(self.load_widget)
        self.main_layout.addStretch()

        self.scroll_widget.setLayout(self.main_layout)


    def add_pdf(self, path : str, page_count : int):
        pdf_widget = PdfItemWidget(path, page_count)
        self.main_layout.insertWidget(len(self.scroll_widget.item_widgets), pdf_widget)
        self.scroll_widget.item_widgets.append(pdf_widget)


    def load_pdf_files(self):
        pdf_paths = select_pdf_paths()
        for path in pdf_paths:
            page_count = get_page_count(path)
            self.add_pdf(path, page_count)


    def generate_pdf(self):
        out_path = select_out_path()

        paths = []
        pages = []

        for widget in self.scroll_widget.item_widgets:
            paths.append(widget.path)
            pages.append((widget.start_page_spin_box.value() - 1, widget.end_page_spin_box.value()))

        merge_pdf(paths, out_path, pages)
        print(f"PDF created at {out_path}")


    def resizeEvent(self, event: QResizeEvent):
        self.generate_button.move(event.size().width() - 100, event.size().height() - 30)



if __name__ == "__main__":
    app = QApplication()

    window = MainWindow()
    window.show()

    app.exec()