from django.forms import FileField
from bookshelf.models import Source
from paper_work.models import Paper
from user_management.models import User
from .models import PaperFile, SourceFile


def save_new_paper_file(file: FileField, paper: Paper, user: User):
    """Create and save new PaperFile obj"""
    new_file = PaperFile(user=user, paper=paper, file=file)
    new_file.save()


def save_new_source_file(file: FileField, source: Source):
    """Create and save new SourceFile obj"""
    new_file = SourceFile(source=source, file=file)
    new_file.save()


def copy_source_file():
    """TODO"""




    return None