from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from paper_work.models import Paper
from file_handling.models import PaperVersion
from work_space.models import WorkSpace, Invitation


def ownership_required(function):
    """Checks if current user is owner of the work_space"""
    def wrapper(request, space_id):

        space = check_work_space(space_id, request.user)
        if space.owner != request.user:
            raise Http404
        
        return function(request, space_id)
    return wrapper


def authorship_required(function):
    """Checks if current user is author of the paper"""
    def wrapper(request, paper_id):

        paper = check_paper(paper_id, request.user)
        if paper.user != request.user:
            raise Http404
        
        return function(request, paper_id)
    return wrapper


def check_work_space(space_id, user):
    """Checks if work_space exists and the user is either its owner or guest"""

    try:
        space = WorkSpace.objects.get(pk=space_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        if space.owner != user and user not in space.guests.all():
            raise Http404
        return space
        

def check_paper(paper_id, user):
    """Checks if user is the author of the given page and page exists"""

    try:
        paper = Paper.objects.get(pk=paper_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(paper.work_space.pk, user)
        return paper


def check_file(file_id, user):
    """Checks if user is the author of the given paper version and this version exists"""

    try:
        file = PaperVersion.objects.get(pk=file_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_paper(file.paper.pk, user)
        return file


def check_invitation(invitation_code):
    """Checks if invitation exists"""

    try:
        return Invitation.objects.get(code=invitation_code)
    except ObjectDoesNotExist:
        raise Http404
