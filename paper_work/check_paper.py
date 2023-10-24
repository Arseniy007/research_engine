from django.core.exceptions import ObjectDoesNotExist

from user_management.models import User
from .models import Paper


def check_paper(user_id, paper_id):
    """Checks if user is the author of the given page and page exists"""
    try:
        user = User.objects.get(pk=user_id)
        paper = Paper.objects.get(pk=paper_id, user=user)

    except ObjectDoesNotExist:
        return False
    else:
        return paper
