from django.core.exceptions import ObjectDoesNotExist

from user_management.models import User
from .models import Paper, PaperVersion


def check_paper(user_id, paper_id):
    """Checks if user is the author of the given page and page exists"""
    try:
        user = User.objects.get(pk=user_id)
        paper = Paper.objects.get(pk=paper_id, user=user)

    except ObjectDoesNotExist:
        return False
    else:
        return paper



def check_file(user_id, file_id):
    """Checks if user is the author of the given paper version and this version exists"""

    try:
        user = User.objects.get(pk=user_id)
        file = PaperVersion.objects.get(pk=file_id, user=user)
    except ObjectDoesNotExist:
        return False
    else:
        return file