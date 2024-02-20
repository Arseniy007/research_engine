from re import search
from zipfile import ZipFile
from PyPDF2 import PdfReader


def count_pages_docx(path_to_file: str) -> int:
    """Get number of pages in .docx file"""
    docx_file = ZipFile(path_to_file)
    file_data = docx_file.read('docProps/app.xml').decode()
    number_of_pages = search(r"<Pages>(\d+)</Pages>", file_data).group(1)
    return int(number_of_pages)


def count_pages_pdf(path_to_file: str) -> int:
    """Get number of pages in pdf file"""
    pdf_file = open(path_to_file, "rb")
    return len(PdfReader(pdf_file).pages)
