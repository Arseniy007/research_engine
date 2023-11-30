from bookshelf.models import Article, Book, Chapter, Source, Webpage
from bookshelf.source_creation import copy_source
from user_management.models import User
from work_space.models import WorkSpace


def create_new_space(owner: User, title: str) -> WorkSpace:
    """Creates new Workpspace obj"""
    new_space = WorkSpace(owner=owner, title=title)
    new_space.save()
    new_space.create_dir()
    return new_space


def copy_space_with_all_sources(original_space: WorkSpace, new_owner: User) -> WorkSpace:
    """Copy work space and all its sources into the new work space"""

    sources = original_space.sources.all()
    if not sources:
        return False
    
    new_space_titile = f"{original_space.title} by {original_space.owner}"
    
    new_space = create_new_space(new_owner, new_space_titile)

    for source in sources:

      copy_source(source, new_space, new_owner)

    
    return new_space
