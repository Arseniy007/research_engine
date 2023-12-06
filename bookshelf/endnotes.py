from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from bookshelf.models import Endnote, Source
from .quoting_apa import quote_source_apa
from .quoting_mla import quote_source_mla


def save_endnotes(source: Source):
    """Creates and saves new Endnote obj for given source"""
    endnotes = Endnote(source=source, apa=quote_source_apa(source), mla=quote_source_mla(source))
    return endnotes.save()


def update_endnotes(source: Source):
    """Updates apa & mla endnotes if source info was altered"""
    endnotes = get_endnotes(source)
    endnotes.apa = quote_source_apa(source)
    endnotes.mla = quote_source_mla(source)
    return endnotes.save(update_fields=("apa", "mla",))


def get_endnotes(source: Source) -> Endnote | Http404:
    """Get endnote for given source"""
    try:
        return Endnote.objects.get(source=source)
    except ObjectDoesNotExist:
        raise Http404
