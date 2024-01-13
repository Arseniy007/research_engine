from django.forms import Form
from bookshelf.forms import ArticleForm, BookForm, ChapterForm, WebpageForm
from utils.data_cleaning import clean_source_form_fields
from .citation_apa import make_article_endnote_apa, make_book_endnote_apa, make_chapter_endnote_apa, make_webpage_endnote_apa
from .citation_mla import make_article_endnote_mla, make_book_endnote_mla, make_chapter_endnote_mla, make_webpage_endnote_mla


def create_input_reference(form: Form, author: str, chapter_author: str=None) -> dict | None:

    # Iterate through all fields and clean its data
    cleaned_data: dict = clean_source_form_fields(form)

    # Add author fields
    cleaned_data["author"] = author
    if chapter_author:
        cleaned_data["chapter_author"] = chapter_author

    match form:
        case BookForm():
            apa_endnote: str = make_book_endnote_apa(cleaned_data)
            mla_endnote: str = make_book_endnote_mla(cleaned_data)
        case ArticleForm():
            apa_endnote: str = make_article_endnote_apa(cleaned_data)
            mla_endnote: str = make_article_endnote_mla(cleaned_data)
        case ChapterForm():
            apa_endnote: str = make_chapter_endnote_apa(cleaned_data)
            mla_endnote: str = make_chapter_endnote_mla(cleaned_data)
        case WebpageForm():
            apa_endnote: str = make_webpage_endnote_apa(cleaned_data)
            mla_endnote: str = make_webpage_endnote_mla(cleaned_data)
        case _:
            return None
    return {"apa_endnote": apa_endnote, "mla_endnote": mla_endnote}
