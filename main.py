from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from pdf_utils import merge_pdf, select_out_path, select_pdf_paths


ENTIRE_GUI = True


if __name__ == "__main__":
    if not ENTIRE_GUI:
        merge_pdf(select_pdf_paths(), select_out_path())
        quit()

    app = QApplication()

    window = MainWindow()
    window.show()

    app.exec()