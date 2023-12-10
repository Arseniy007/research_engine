from typing import Callable
from .models import Article, Book, Chapter, Source, Webpage
from quoting.quoting_apa import quote_article_apa, quote_book_apa, quote_chapter_apa, quote_webpage_apa
from quoting.quoting_mla import quote_article_mla, quote_book_mla, quote_chapter_mla, quote_webpage_mla


def quote_source_apa(source: Source) -> Callable | bool:
    """Get source type and call corresponding func"""

    source_type: type(object) = source.cast()
    match source_type:
        # Go to child model and turn it into dict in order to call needed func
        case Book():
            book: dict = vars(source.book)
            return quote_book_apa(book)
        case Article():
            article: dict = vars(source.article)
            return quote_article_apa(article)
        case Chapter():
            chapter: dict = vars(source.chapter)
            return quote_chapter_apa(chapter)
        case Webpage():
            webpage: dict = source.webpage
            return quote_webpage_apa(webpage)
        case _:
            return None


def quote_source_mla(source: Source) -> Callable | bool:
    """Get source type and call corresponding func"""
    
    source_type: type(object) = source.cast()
    match source_type:
        # Go to child model and turn it into dict in order to call needed func
        case Book():
            book: dict = vars(source.book)
            return quote_book_mla(book)
        case Article():
            article: dict = vars(source.article)
            return quote_article_mla(article)
        case Chapter():
            chapter: dict = vars(source.chapter)
            return quote_chapter_mla(chapter)
        case Webpage():
            webpage: dict = source.webpage
            return quote_webpage_mla(webpage)
        case _:
            return None

