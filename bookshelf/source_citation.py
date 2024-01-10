from typing import Callable
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from .models import Article, Book, Chapter, Endnote, Source, Webpage
from citation.quoting_apa import make_article_endnote_apa, make_book_endnote_apa, make_chapter_endnote_apa, make_webpage_endnote_apa
from citation.quoting_mla import make_article_endnote_mla, make_book_endnote_mla, make_chapter_endnote_mla, make_webpage_endnote_mla


def create_endnotes(source: Source):
    """Creates and saves new Endnote obj for given source"""
    endnotes = Endnote(source=source, apa=make_source_endnote_apa(source), mla=make_source_endnote_mla(source))
    return endnotes.save()


def update_endnotes(source: Source):
    """Updates apa & mla endnotes if source info was altered"""
    endnotes = get_endnotes(source)
    endnotes.apa = make_source_endnote_apa(source)
    endnotes.mla = make_source_endnote_mla(source)
    return endnotes.save(update_fields=("apa", "mla",))


def get_endnotes(source: Source) -> Endnote | Http404:
    """Get endnote for given source"""
    try:
        return Endnote.objects.get(source=source)
    except ObjectDoesNotExist:
        raise Http404


def make_source_endnote_apa(source: Source) -> Callable | bool:
    """Get source type and call corresponding func"""

    source_type: type(object) = source.cast()
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
            webpage: dict = source.webpage
            return make_webpage_endnote_apa(webpage)
        case _:
            return None


def make_source_endnote_mla(source: Source) -> Callable | bool:
    """Get source type and call corresponding func"""
    
    source_type: type(object) = source.cast()
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
            webpage: dict = source.webpage
            return make_webpage_endnote_mla(webpage)
        case _:
            return None

