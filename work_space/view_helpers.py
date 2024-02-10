from django.forms.models import model_to_dict
from bookshelf.models import Source
from paper_work.models import Paper
from .models import WorkSpace


def get_work_space_sources(space: WorkSpace) -> list:
    """Get all sources related to given workspace + add some additional info about them"""

    sources: list = []
    for source in space.sources.all():
        source: Source
        source_dict: dict = model_to_dict(source)

        source_dict["type"] = source.get_type()

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
