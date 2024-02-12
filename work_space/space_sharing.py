from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from utils.code_generator import generate_code
from .models import Invitation, ShareSourcesCode, WorkSpace


def generate_invitation(space: WorkSpace) -> str:
    """Generates random invitation code and creates its object"""

    # Make sure invitation texts never repeat
    while True:
        # Generate random string
        invitation_code = generate_code()
        try:
            new_invitation = Invitation(code=invitation_code, work_space=space)
            new_invitation.save()
        except IntegrityError:
            # Generate new code in case of repetition
            continue
        else:
            return invitation_code


def share_sources(space: WorkSpace) -> None:
    """Mark space as shared and create new sharing code"""

    # Delete sharing code if it was already made
    sharing_code = get_sources_sharing_code(space)
    if sharing_code:
        sharing_code.delete()

    # Create new sharing code
    new_sharing_code = ShareSourcesCode(work_space=space, code=generate_code())
    return new_sharing_code.save()


def get_sources_sharing_code(space: WorkSpace) -> ShareSourcesCode | None:
    """Check if space is shared and there is ShareSourcesCode obj"""
    try:
        return ShareSourcesCode.objects.get(work_space=space)
    except ObjectDoesNotExist:
        return None
