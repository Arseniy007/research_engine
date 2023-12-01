from .models import Article, Book, Chapter, Source, Webpage
from .source_creation import save_endnotes
from user_management.models import User
from work_space.models import WorkSpace


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
    if source.file:
        source.file = copy_source_file_info(source, new_space, new_owner.pk)
    source.save(update_fields=("file",))

    # Copy all quotes related to original source if necessary
    if source_quotes:
        for quote in source_quotes:
            quote.pk, quote.source = None, source
            quote._state.adding = True
            quote.save()

    # Create new Endnote obj based on new source
    save_endnotes(source)
    return source


def copy_source_file_info(source: Source, new_space: WorkSpace, new_owner_id: int) -> str:
    """Returns a new path to the copied file"""
    space_path = new_space.get_base_dir()
    source_id, user_id = source.pk, new_owner_id
    filename = source.file_name()
    return f"{space_path}/sources/user_{user_id}/source_{source_id}/{filename}"
