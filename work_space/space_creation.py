from bookshelf.models import Article, Book, Chapter, Source, Webpage
from user_management.models import User
from work_space.models import WorkSpace


def create_new_space(owner: User, title: str) -> WorkSpace:
    """Creates new Workpspace obj"""
    new_space = WorkSpace(owner=owner, title=title)
    new_space.save()
    new_space.create_dir()
    return new_space


def copy_space_with_sources(original_space: WorkSpace, new_owner: User) -> WorkSpace:
    """Copy work space and all its sources into the new work space"""

    sources = original_space.sources.all()
    if not sources:
        return False
    
    new_space_titile = f"{original_space.title} by {original_space.owner}"
    
    new_space = create_new_space(new_owner, new_space_titile)

    for source in sources:

      copy_source(source, new_space)

    
    return new_space
    



def copy_source(source: Source, new_space: WorkSpace) -> Source:
    """Copy source and change its work space"""

    source.pk = None
    source.id = None
    source.work_space = new_space
    source._state.adding = True
    source.save()



    return None
    source_type = source.cast()
    match source_type:
        case Book():
            pass
        case Article():
            pass
        case Chapter():
            pass
        case Webpage():
            pass
        case _:
            return None