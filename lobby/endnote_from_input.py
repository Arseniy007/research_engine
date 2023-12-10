from django.forms import Form
from bookshelf.forms import ArticleForm, BookForm, ChapterForm, WebpageForm
from utils.data_cleaning import clean_source_form_fields
from quoting.quoting_apa import quote_article_apa, quote_book_apa, quote_chapter_apa, quote_webpage_apa
from quoting.quoting_mla import quote_article_mla, quote_book_mla, quote_chapter_mla, quote_webpage_mla


def quote_input_source(form: Form, chapter_author: str=None) -> dict | None:

    # Iterate through all fields and clean its data
    cleaned_data: dict = clean_source_form_fields(form)
    if chapter_author:
        cleaned_data["chapter_author"] = chapter_author

    match form:
        case BookForm():
            apa_endnote: str = quote_book_apa(cleaned_data)
            mla_endnote: str = quote_book_mla(cleaned_data)
        case ArticleForm():
            apa_endnote: str = quote_article_apa(cleaned_data)
            mla_endnote: str = quote_article_mla(cleaned_data)
        case ChapterForm():
            apa_endnote: str = quote_chapter_apa(cleaned_data)
            mla_endnote: str = quote_chapter_mla(cleaned_data)
        case WebpageForm():
            apa_endnote: str = quote_webpage_apa(cleaned_data)
            mla_endnote: str = quote_webpage_mla(cleaned_data)
        case _:
            return None
    return {"apa_endnote": apa_endnote, "mla_endnote": mla_endnote}
