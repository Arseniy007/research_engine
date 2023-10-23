from django.core.exceptions import ObjectDoesNotExist

from .models import Paper, PaperVersion



def save_paper_version(paper_id, text):

    try:
        paper = Paper.objects.get(pk=paper_id)
    except ObjectDoesNotExist:
        return False
    else:
        new_version = PaperVersion(paper=paper, text=text)
        new_version.save()

    return True


def save_paper(user, title):

    new_paper = Paper(user=user, title=title)
    new_paper.save()
    

"""
def get_user_paper_directory_path(user_id, title):

    return f"../uploads/papers/user_{user_id}/{title}/%Y/%m/%d/"
"""