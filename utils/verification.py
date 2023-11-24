import requests
from requests.exceptions import RequestException
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from bookshelf.models import Article, Book, Chapter, Endnote, Quote, Source, Webpage
from file_handling.models import PaperVersion
from paper_work.models import Paper
from user_management.models import User
from work_space.models import Comment, Invitation, WorkSpace


def check_work_space(space_id: int, user: User) -> WorkSpace:
    """Checks if work_space exists and the user is either its owner or guest"""
    try:
        space = WorkSpace.objects.get(pk=space_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        if space.owner != user and user not in space.guests.all():
            raise PermissionDenied
    return space
        

def check_paper(paper_id: int, user: User) -> Paper:
    """Checks if user is the author of the given page and page exists"""
    try:
        paper = Paper.objects.get(pk=paper_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(paper.work_space.pk, user)
    return paper


def check_file(file_id: int, user: User) -> PaperVersion:
    """Checks if user is the author of the given paper version and this version exists"""
    try:
        file = PaperVersion.objects.get(pk=file_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_paper(file.paper.pk, user)
    return file


def check_source(source_id: int, user: User) -> Source:
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
            case Chapter():
                check_work_space(source.chapter.work_space.pk, user)
            case Webpage():
                check_work_space(source.webpage.work_space.pk, user)
            case _:
                pass
    finally:
        return source


def check_endnote(endnote_id: int, user: User) -> Endnote:
    """Checks if endnote exists"""
    try:
        endnote = Endnote.objects.get(pk=endnote_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(endnote.source.work_space.pk, user)
    return endnote


def get_endnotes(source: Source) -> Endnote:
    """Get endnote for given source"""
    try:
        return Endnote.objects.get(source=source)
    except ObjectDoesNotExist:
        raise Http404


def check_quote(quote_id: int, user: User) -> Quote:
    """Checks if quote exists"""
    try:
        quote = Quote.objects.get(pk=quote_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(quote.source.work_space.pk, user)
    return quote
    

def check_comment(comment_id: int, user: User) -> Comment:
    """Checks if comments exitst"""
    try:
        comment = Comment.objects.get(pk=comment_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(comment.work_space.pk, user)
    return comment


def check_invitation(invitation_code: str) -> Invitation:
    """Checks if invitation exists"""
    try:
        return Invitation.objects.get(code=invitation_code)
    except ObjectDoesNotExist:
        raise Http404


def check_link(link: str) -> bool:
    """Checks if given link is indeed a link and gets you to a real webpage"""
    try: 
        response = requests.get(link)
    except RequestException:
        return False
    else:
        return response.ok
