from file_handling.file_saving import save_new_source_file
from file_handling.models import SourceFile
from user_management.models import User
from work_space.models import WorkSpace
from .models import Article, Book, Chapter, Source, Webpage
from .source_citation import create_source_reference


def copy_source(source: Source, new_space: WorkSpace, new_owner: User) -> Source:
    """Copy source and change its work space"""

    # Go down to source child obj
    source_type = source.cast()
    match source_type:
        case Book():
            source = source.book
        case Article():
            source = source.article
        case Chapter():
            source = source.chapter
        case Webpage():
            source = source.webpage
        case _:
            return None
    
    # Save all quotes related to the source
    source_quotes = source.quotes.all()

    # Copy the given source and alter its key fields
    source.pk, source.id = None, None
    source.work_space, source.user = new_space, new_owner
    source._state.adding = True
    source.save()

    # Change file info, if file was uploaded
    source_file: SourceFile | None = source.get_file()
    if source_file:
        save_new_source_file(source_file.file, source)

    # Copy all quotes related to original source if necessary
    if source_quotes:
        for quote in source_quotes:
            quote.pk, quote.source = None, source
            quote._state.adding = True
            quote.save()

    # Create new Reference obj based on new source
    create_source_reference(source)
    return source


# Do I need it?
def copy_source_file_info(source: Source, new_space: WorkSpace, new_owner_id: int) -> str:
    """Returns a new path to the copied file"""
    space_path = new_space.get_base_dir()
    source_id, user_id = source.pk, new_owner_id
    filename = source.file_name()
    return f"{space_path}/sources/user_{user_id}/source_{source_id}/{filename}"
