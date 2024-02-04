from django.forms.models import model_to_dict
from work_space.models import WorkSpace
from .models import Article, Book, Chapter, Source, Webpage


def get_work_space_sources(space: WorkSpace) -> list:
    """Get all sources related to given workspace + add some additional info about them"""

    sources: list = []
    for source in space.sources.all():
        source: Source
        source_dict: dict = model_to_dict(source)

        source_dict["type"] = get_source_type(source)

        if source.has_file:
            source_dict["file_id"] = source.get_file().pk
        else:
            source_dict["file_id"] = None
        if source.quotes.all():
            source_dict["has_quotes"] = True
        else:
            source_dict["has_quotes"] = False
        sources.append(source_dict)

    return sources


def get_source_type(source: Source) -> str:
    """Return str with source type"""

    source_type = source.cast()
    match source_type:
        case Book():
            return "book"
        case Article():
            return"article"
        case Chapter():
            return "chapter"
        case Webpage():
            return "webpage"
