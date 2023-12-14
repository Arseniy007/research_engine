import requests
from requests.exceptions import RequestException
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from bookshelf.models import Article, Book, Chapter, Endnote, Quote, Source, Webpage
from file_handling.models import PaperVersion
from paper_work.models import Paper
from profile_page.models import ProfilePage
from user_management.models import PasswordResetCode, User
from work_space_parts.models import Comment, Link, Note
from work_space.models import Invitation, ShareSourcesCode, WorkSpace


def check_work_space(space_id: int, user: User) -> WorkSpace | Http404 | PermissionDenied:
    """Checks if work_space exists and the user is either its owner or guest"""
    try:
        space = WorkSpace.objects.get(pk=space_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        if space.owner != user and user not in space.guests.all():
            raise PermissionDenied
    return space
        

def check_paper(paper_id: int, user: User) -> Paper | Http404:
    """Checks if user is the author of the given page and page exists"""
    try:
        paper = Paper.objects.get(pk=paper_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(paper.work_space.pk, user)
    return paper


def check_file(file_id: int, user: User) -> PaperVersion | Http404:
    """Checks if user is the author of the given paper version and this version exists"""
    try:
        file = PaperVersion.objects.get(pk=file_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_paper(file.paper.pk, user)
    return file


def check_source(source_id: int, user: User) -> Source | Http404:
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
                return None
    return source


def check_quote(quote_id: int, user: User) -> Quote | Http404:
    """Checks if quote exists"""
    try:
        quote = Quote.objects.get(pk=quote_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(quote.source.work_space.pk, user)
    return quote
    

def check_comment(comment_id: int, user: User) -> Comment | Http404:
    """Checks if comments exits"""
    try:
        comment = Comment.objects.get(pk=comment_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(comment.work_space.pk, user)
    return comment


def check_note(note_id: int, user: User) -> Note | Http404:
    """Checks if note exists"""
    try:
        note = Note.objects.get(pk=note_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(note.work_space.pk, user)
    return note


def check_space_link(link_id: int, user: User) -> Link | Http404:
    """Checks if link exists"""
    try:
        link = Link.objects.get(pk=link_id)
    except ObjectDoesNotExist:
        raise Http404
    else:
        check_work_space(link.work_space.pk, user)
    return link


def check_profile(profile_id: int) -> ProfilePage | Http404:
    """Checks if given user exists"""
    try:
        return ProfilePage.objects.get(pk=profile_id)
    except ObjectDoesNotExist:
        raise Http404


def check_invitation(invitation_code: str) -> Invitation | Http404:
    """Checks if invitation exists"""
    try:
        return Invitation.objects.get(code=invitation_code)
    except ObjectDoesNotExist:
        raise Http404


def check_share_sources_code(share_space_code: str) -> ShareSourcesCode | Http404:
    """Checks if share_space_code exists"""
    try:
        return ShareSourcesCode.objects.get(code=share_space_code)
    except ObjectDoesNotExist:
        raise Http404


def check_reset_password_code(reset_code: str, user: User) -> PasswordResetCode | None:
    """Checks if reset-password code exists"""
    try:
        return PasswordResetCode.objects.get(user=user, code=reset_code)
    except ObjectDoesNotExist:
        return None


def check_link(link: str) -> bool:
    """Checks if given link is indeed a link and gets you to a real webpage"""
    try: 
        response = requests.get(link)
    except RequestException:
        return False
    else:
        return response.ok
