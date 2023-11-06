from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404

from bookshelf.models import Book, Quote
from file_handling.models import PaperVersion
from paper_work.models import Paper
from work_space.models import WorkSpace, Invitation


def check_work_space(space_id, user):
    """Checks if work_space exists and the user is either its owner or guest"""

    try:
        space = WorkSpace.objects.get(pk=space_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        if space.owner != user and user not in space.guests.all():
            raise PermissionDenied
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


def check_book(book_id, user):
    """Checks if book exists"""

    try:
        book = Book.objects.get(pk=book_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(book.work_space.pk, user)
        return book
    

def check_quote(quote_id, user):
    """Checks if quote exists and user added it"""

    try:
        quote = Quote.objects.get(pk=quote_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_book(quote.book.pk, user)
        return quote


def check_invitation(invitation_code):
    """Checks if invitation exists"""

    try:
        return Invitation.objects.get(code=invitation_code)
    except ObjectDoesNotExist:
        raise Http404
