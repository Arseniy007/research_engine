from user_management.models import User
from work_space.models import WorkSpace


def create_new_space(owner: User, title: str) -> WorkSpace:
    """Creates new Workpspace obj"""
    new_space = WorkSpace(owner=owner, title=title)
    new_space.save()
    return new_space.create_dir()
