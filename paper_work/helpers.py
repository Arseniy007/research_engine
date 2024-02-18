from user_management.helpers import get_user_work_spaces
from user_management.models import User
from work_space.models import WorkSpace
from .bibliography import create_bibliography
from file_handling.models import PaperFile
from .models import Paper


def create_new_paper(space: WorkSpace, user: User, title: str, citation_style: str) -> Paper:
    """Save new Paper object"""
    new_paper = Paper(work_space=space, user=user, title=title, citation_style=citation_style)
    new_paper.save()
    create_bibliography(new_paper)
    return new_paper


def rename_paper_obj(paper: Paper, new_title: str):
    """Change title fields at paper obj"""
    paper.title = new_title
    return paper.save(update_fields=("title",))


def transfer_paper(paper: Paper, new_space: WorkSpace):
    """Change work_space field at paper obj"""
    paper.work_space = new_space
    return paper.save(update_fields=("work_space",))


def change_citation_style(paper: Paper) -> str:
    """Change citation_style field at paper obj"""

    if paper.citation_style == "APA":
        new_style = "MLA"
    else:
        new_style = "APA"
    paper.citation_style = new_style
    paper.save(update_fields=("citation_style",))
    return new_style


def get_available_spaces(paper: Paper, user: User) -> list:
    """Get all user workspaces except for which paper is in"""
    users_spaces = get_user_work_spaces(user)
    return [space for space in users_spaces if space != paper.work_space]


def get_paper_files(paper: Paper):
    """Get all uploaded paper files in reversed order"""
    return PaperFile.objects.filter(paper=paper).order_by("-version_number")


def get_chosen_source_ids(paper: Paper) -> list:
    """Get id of every chosen source"""
    return [source.pk for source in paper.sources.all()]
