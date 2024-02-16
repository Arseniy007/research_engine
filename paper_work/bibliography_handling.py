from docx import Document

from .models import Bibliography, Paper

from bookshelf.source_citation import get_source_reference



def create_bibliography(paper: Paper) -> Bibliography:
    """"""

    endnotes = [get_source_reference(source).endnote_apa for source in paper.sources.all()]
    print(*endnotes, sep="\n")



def append_bibliography_docx(path_to_file: str, bibliography: str):
    """"""
    file = Document(path_to_file)
    file.add_paragraph(bibliography)
    file.save(path_to_file)


