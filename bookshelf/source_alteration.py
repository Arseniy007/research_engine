from django import forms
from .dates import validate_date
from .forms import AlterWebpageForm
from .models import Article, Book, Chapter, Source, Webpage
from .source_creation import clean_text_data
from .quoting_apa import quote_source_apa
from .quoting_mla import quote_source_mla
from utils.verification import check_link, get_endnotes


def alter_source(source: Source, form: forms.Form):
    """Get source type and call right func"""
    source_type = source.cast()
    match source_type:
        case Book():
            return update_source_fields(source.book, form)
        case Article():
            return update_source_fields(source.article, form)
        case Chapter():
            return update_source_fields(source.chapter, form)
        case Webpage():
            return update_webpage_fields(source.webpage, form)
        case _:
            return None


def update_source_fields(source: Book | Article | Chapter, form: forms.Form):
    """Alter book / article / chapter objs."""
    for field in form.fields:
        # Ignrore "source_type" field
        if field != "source_type":
            info = form.cleaned_data[field]
            # Check if field was indeed altered
            if source.__getattribute__(field) != info:
                if type(info) == str:
                    info = clean_text_data(info)
                # Update field and save obj
                source.__setattr__(field, info)
                source.save(update_fields=(field,))
    return update_endnotes(source)


def update_webpage_fields(webpage: Webpage, form: AlterWebpageForm):
    """Alter webpage obj."""
    for field in form.fields:
        # Ignrore "source_type" field
        if field != "source_type":
            info = form.cleaned_data[field]
            # Check if field was indeed altered
            if webpage.__getattribute__(field) != info:
                if type(info) == str:
                    info = clean_text_data(info)
                if field == "date":
                    if not validate_date(info):
                        # TODO
                        pass
                elif field == "page_url":
                    if not check_link(info):
                        # TODO
                        pass
                # Update field and save obj
                webpage.__setattr__(field, info)
                webpage.save(update_fields=(field,))
    return update_endnotes(webpage)


def update_endnotes(source: Source):
    """Updates apa & mla endnotes if source info was altered"""
    endnotes = get_endnotes(source)
    endnotes.apa = quote_source_apa(source)
    endnotes.mla = quote_source_mla(source)
    return endnotes.save(update_fields=("apa", "mla",))
