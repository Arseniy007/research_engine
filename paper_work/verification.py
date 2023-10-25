from django.core.exceptions import ObjectDoesNotExist

from .models import Paper, PaperVersion


def check_paper(user, paper_id):
    """Checks if user is the author of the given page and page exists"""
    try:
        paper = Paper.objects.get(pk=paper_id, user=user)

    except ObjectDoesNotExist:
        return False
    else:
        return paper


def check_file(user, file_id):
    """Checks if user is the author of the given paper version and this version exists"""

    try:
        file = PaperVersion.objects.get(pk=file_id, user=user)
    except ObjectDoesNotExist:
        return False
    else:
        return file
