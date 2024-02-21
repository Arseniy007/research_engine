from django.forms.models import model_to_dict
from bookshelf.models import Source
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
        sources.append(source_dict)

    return sources


def check_emptiness(space: WorkSpace) -> bool:
    """Check if space is empty or not"""
    # Get all sources and papers in given work space
    sources = space.sources.all()
    papers = space.papers.filter(archived=False)

    if not sources and not papers:
        return True
    return False
