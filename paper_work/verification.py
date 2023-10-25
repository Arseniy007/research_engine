from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .models import Paper, PaperVersion


def check_paper(paper_id, user):
    """Checks if user is the author of the given page and page exists"""

    try:
        paper = Paper.objects.get(pk=paper_id, user=user)
    except ObjectDoesNotExist:
        raise Http404
    else:
        return paper


def check_file(file_id, user):
    """Checks if user is the author of the given paper version and this version exists"""

    try:
        file = PaperVersion.objects.get(pk=file_id, user=user)
    except ObjectDoesNotExist:
        raise Http404
    else:
        return file
