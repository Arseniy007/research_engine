from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from bookshelf.models import Article, Book, Chapter, Source, Webpage
from file_handling.models import PaperFile, SourceFile
from paper_work.models import Paper
from user_management.models import PasswordResetCode, User
from work_space.models import Invitation, ShareSourcesCode, WorkSpace


def check_work_space(space_id: int, user: User) -> WorkSpace | Http404 | PermissionDenied:
    """Checks if work_space exists and the user is either its owner or member"""
    try:
        space = WorkSpace.objects.get(pk=space_id)
    except ObjectDoesNotExist as e:
        raise Http404 from e
    else:
        if space.owner != user and user not in space.members.all():
            raise PermissionDenied
    return space


def check_source(source_id: int, user: User) -> Source | Http404:
    """Checks source, its type and work space"""
    try:
        source = Source.objects.get(pk=source_id)
    except ObjectDoesNotExist as e:
        raise Http404 from e
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


def check_user(user_id: int) -> User | Http404:
    """Check if user with given id exists"""
    try:
        return User.objects.get(pk=user_id)
    except ObjectDoesNotExist as e:
        raise Http404 from e


def check_paper(paper_id: int, user: User) -> Paper | Http404:
    """Checks if paper exists and user has access to it"""
    try:
        paper = Paper.objects.get(pk=paper_id)
    except ObjectDoesNotExist as e:
        raise Http404 from e
    else:
        check_work_space(paper.work_space.pk, user)
    return paper


def check_source_file(file_id: int, user: User) -> SourceFile | Http404:
    """Check if source file exists and user has access to it"""
    try:
        file = SourceFile.objects.get(pk=file_id)
    except ObjectDoesNotExist as e:
        raise Http404 from e
    else:
        check_source(file.source.pk, user)
    return file


def check_paper_file(file_id: int, user: User) -> PaperFile | Http404:
    """Checks if this file exists"""
    try:
        file = PaperFile.objects.get(pk=file_id)
    except ObjectDoesNotExist as e:
        raise Http404 from e
    else:
        check_paper(file.paper.pk, user)
    return file


def check_invitation(invitation_code: str) -> Invitation | bool:
    """Checks if invitation exists"""
    try:
        return Invitation.objects.get(code=invitation_code)
    except ObjectDoesNotExist:
        return False


def check_share_sources_code(share_space_code: str) -> ShareSourcesCode | bool:
    """Checks if share_space_code exists"""
    try:
        return ShareSourcesCode.objects.get(code=share_space_code)
    except ObjectDoesNotExist:
        return False


def check_reset_password_code(reset_code: str, user: User) -> PasswordResetCode | None:
    """Checks if reset-password code exists"""
    try:
        return PasswordResetCode.objects.get(code=reset_code, user=user)
    except ObjectDoesNotExist:
        return None
