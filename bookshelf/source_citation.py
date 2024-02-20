from typing import Callable
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from citation.citation_apa import (
    make_article_endnote_apa, make_book_endnote_apa,
    make_chapter_endnote_apa, make_webpage_endnote_apa
)
from citation.citation_mla import (
    make_article_endnote_mla, make_book_endnote_mla,
    make_chapter_endnote_mla, make_webpage_endnote_mla
)
from .models import Article, Book, Chapter, Reference, Source, Webpage


def create_source_reference(source: Source):
    """Creates and saves new Endnote obj for given source"""
    reference = Reference(source=source,
                          endnote_apa=make_source_endnote_apa(source),
                          endnote_mla=make_source_endnote_mla(source))
    return reference.save()


def update_source_reference(source: Source):
    """Updates apa & mla endnotes if source info was altered"""
    reference = get_source_reference(source)
    reference.endnote_apa = make_source_endnote_apa(source)
    reference.endnote_mla = make_source_endnote_mla(source)
    return reference.save(update_fields=("endnote_apa", "endnote_mla",))


def get_source_reference(source: Source) -> Reference | Http404:
    """Get endnote for given source"""
    try:
        return Reference.objects.get(source=source)
    except ObjectDoesNotExist as e:
        raise Http404 from e


def make_source_endnote_apa(source: Source) -> Callable | bool:
    """Get source type and call corresponding func"""

    source_type: object = source.cast()
    match source_type:
        # Go to child model and turn it into dict in order to call needed func
        case Book():
            book: dict = vars(source.book)
            return make_book_endnote_apa(book)
        case Article():
            article: dict = vars(source.article)
            return make_article_endnote_apa(article)
        case Chapter():
            chapter: dict = vars(source.chapter)
            return make_chapter_endnote_apa(chapter)
        case Webpage():
            webpage: dict = vars(source.webpage)
            return make_webpage_endnote_apa(webpage)
        case _:
            return None


def make_source_endnote_mla(source: Source) -> Callable | bool:
    """Get source type and call corresponding func"""

    source_type: object = source.cast()
    match source_type:
        # Go to child model and turn it into dict in order to call needed func
        case Book():
            book: dict = vars(source.book)
            return make_book_endnote_mla(book)
        case Article():
            article: dict = vars(source.article)
            return make_article_endnote_mla(article)
        case Chapter():
            chapter: dict = vars(source.chapter)
            return make_chapter_endnote_mla(chapter)
        case Webpage():
            webpage: dict = vars(source.webpage)
            return make_webpage_endnote_mla(webpage)
        case _:
            return None
