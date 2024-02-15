from bookshelf.models import Source
from paper_work.models import Paper
from user_management.models import User
from .models import PaperFile, SourceFile


def save_new_paper_file(paper: Paper, user: User, file, commit_text: str | None):
    """Create and save new PaperFile obj"""
    new_file = PaperFile(user=user, paper=paper, file=file, commit_text=commit_text)
    new_file.save()


def save_new_source_file(source: Source, file):
    """Create and save new SourceFile obj"""
    new_file = SourceFile(source=source, file=file)
    new_file.save()
    source.has_file = True
    source.save(update_fields=("has_file",))
