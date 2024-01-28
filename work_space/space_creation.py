from bookshelf.source_copying import copy_source
from user_management.models import User
from work_space.models import WorkSpace


def create_new_space(owner: User, title: str) -> WorkSpace:
    """Creates new Workspace obj"""
    new_space = WorkSpace(owner=owner, title=title)
    new_space.save()
    new_space.create_dir()
    return new_space


def copy_space_with_all_sources(original_space: WorkSpace, new_owner: User) -> WorkSpace:
    """Copy work space and all its sources into the new work space"""

    # Get all original sources
    original_sources = original_space.sources.all()
    if not original_sources:
        return False
    
    # Create new Workspace obj
    new_space_title = f"{original_space.title} by {original_space.owner}"
    new_space = create_new_space(new_owner, new_space_title)

    # Copy all sources into db
    for source in original_sources:
        copy_source(source, new_space, new_owner)

    # Return new Workspace obj
    return new_space
