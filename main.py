from PyPDF2 import PdfMerger
from tkinter import Tk
from tkinter import filedialog

def merge_pdf(pdf_paths : list, out_path : str):
    merger = PdfMerger()
    for pdf in pdf_paths:
        assert(type(pdf) == str)
        merger.append(pdf)
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


if __name__ == "__main__":
    merge_pdf(select_pdf_paths(), select_out_path())