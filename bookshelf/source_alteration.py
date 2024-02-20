from typing import Callable
from django import forms
from utils.data_cleaning import clean_text_data
from .source_citation import update_source_reference
from .forms import AlterWebpageForm
from .models import Article, Book, Chapter, Source, Webpage


def alter_source(source: Source, form: forms.Form) -> Callable | None:
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


def update_source_fields(source: Book | Article | Chapter, form: forms.Form) -> Source:
    """Alter book / article / chapter objs."""
    for field in form.fields:
        # Ignore "source_type" field
        if field not in ("source_type", "number_of_authors",):
            info = form.cleaned_data[field]
            # Check if field was indeed altered
            if getattr(source, field) != info:
                if isinstance(info, str):
                    info = clean_text_data(info)
                # Update field and save obj
                setattr(source, field, info)
                source.save(update_fields=(field,))
    update_source_reference(source)
    return source


def update_webpage_fields(webpage: Webpage, form: AlterWebpageForm) -> Webpage:
    """Alter webpage obj."""
    for field in form.fields:
        # Ignore "source_type" field
        if field not in ("source_type", "number_of_authors",):
            info = form.cleaned_data[field]
            # Check if field was indeed altered
            if getattr(webpage, field) != info:
                if isinstance(info, str):
                    info = clean_text_data(info)
                # Update field and save obj
                setattr(webpage, field, info)
                webpage.save(update_fields=(field,))
    update_source_reference(webpage)
    return webpage
