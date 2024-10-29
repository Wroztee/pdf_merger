from PyPDF2 import PdfMerger, PdfReader
from tkinter import Tk
from tkinter import filedialog

def merge_pdf(pdf_paths : list, out_path : str, pages : list = None):
    merger = PdfMerger()
    for i in range(len(pdf_paths)):
        pdf = pdf_paths[i]
        assert(type(pdf) == str)
        if pages is None or pages[i] is None:
            merger.append(pdf)
        else:
            merger.append(pdf, pages=pages[i])
    merger.write(out_path)
    merger.close()


def select_pdf_paths(start_dir : str = "./") -> list:
    root = Tk()
    root.withdraw()
    pdf_paths = filedialog.askopenfilenames(filetypes=[("Portable Document Format", "*.pdf")], initialdir=start_dir)
    return pdf_paths


def select_out_path(start_dir : str = "./") -> str:
    root = Tk()
    root.withdraw()
    out_path = filedialog.asksaveasfilename(filetypes=[("Portable Document Format", "*.pdf")], initialdir=start_dir)
    if out_path[-4:] != ".pdf":
        out_path += ".pdf"
    return out_path


def get_page_count(pdf_path : str) -> int:
    file = open(pdf_path, "rb")
    reader = PdfReader(file)
    page_count = len(reader.pages)
    file.close()
    return page_count


if __name__ == "__main__":
    merge_pdf(select_pdf_paths(), select_out_path())