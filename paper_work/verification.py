from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .models import Paper, PaperVersion
from work_space.models import WorkSpace


def check_work_space(space_id, user):
    """Checks if work_space exists and the user is its owner"""

    try:
        return WorkSpace.objects.get(pk=space_id, owner=user)
    except ObjectDoesNotExist:
        raise Http404


def check_paper(paper_id, user):
    """Checks if user is the author of the given page and page exists"""

    try:
        return Paper.objects.get(pk=paper_id, user=user)
    except ObjectDoesNotExist:
        raise Http404


def check_file(file_id, user):
    """Checks if user is the author of the given paper version and this version exists"""

    try:
        file = PaperVersion.objects.get(pk=file_id)
        Paper.objects.get(pk=file.paper.pk, user=user)
    except ObjectDoesNotExist:
        raise Http404
    else:
        return file
