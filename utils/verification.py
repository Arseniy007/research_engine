from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404

import requests

from bookshelf.models import Source, Article, Book, Quote, Website, Endnote
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


def check_source(source_id, user):
    """Checks source, its type and work space"""
    try:
        source = Source.objects.get(pk=source_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        source_type = source.cast()
        match source_type:
            case Book():
                check_work_space(source.book.work_space.pk, user)
            case Article():
                check_work_space(source.article.work_space.pk, user)
            case Website():
                check_work_space(source.website.work_space.pk, user)
            case _:
                pass
    finally:
        return source


def check_endnote(endnote_id, user):

    try:
        endnote = Endnote.objects.get(pk=endnote_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(endnote.source.work_space.pk, user)
        return endnote


def get_endnotes(source: Source):
    """Get endnote for given source"""

    try:
        return Endnote.objects.get(source=source)
    except ObjectDoesNotExist:
        raise Http404


def check_quote(quote_id, user):
    """Checks if quote exists"""
    try:
        quote = Quote.objects.get(pk=quote_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(quote.source.work_space.pk, user)
        return quote


def check_invitation(invitation_code: str):
    """Checks if invitation exists"""
    try:
        return Invitation.objects.get(code=invitation_code)
    except ObjectDoesNotExist:
        raise Http404


def check_link(link: str) -> bool:
    """Checks if given link is indeed a link and gets you to a real webpage"""
    try: 
        response = requests.get(link)
    except requests.exceptions.RequestException:
        return False
    else:
        return response.ok
