from random import SystemRandom
from string import ascii_lowercase, ascii_uppercase, digits
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Invitation, ShareSourcesCode, WorkSpace


# String with all ascii char options for the generator
POPULATION = ascii_lowercase + ascii_uppercase + digits

# Numbers of characters in invitation code
LENGTH_OF_STRING = 15


def generate_code() -> str:
    """Generate random string using chars and digits"""
    return "".join([SystemRandom().choice(POPULATION) for _ in range(LENGTH_OF_STRING)])


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

    # Mark that space sources are shared
    if not space.share_sources:
        space.share_sources = True
        space.save(update_fields=("share_sources",))

    # Delete sharing code if it was already made
    sharing_code = get_space_sharing_code(space)
    if sharing_code:
        sharing_code.delete()
    
    # Create new sharing code
    new_sharing_code = ShareSourcesCode(work_space=space, code=generate_code())
    return new_sharing_code.save()


def stop_sharing_sources(space: WorkSpace) -> None:
    """Mark sharing sources as False and delete sharing code obj"""

    # Mark that space sources are not shared
    if space.share_sources:
        space.share_sources = False
        space.save(update_fields=("share_sources",))

    # Delete sharing code if it was already made
    sharing_code = get_space_sharing_code(space)
    if sharing_code:
        sharing_code.delete()


def get_space_sharing_code(space: WorkSpace) -> ShareSourcesCode | None:
    """Check if space is shared and there is ShareSourcesCode obj"""
    try:
        return ShareSourcesCode.objects.get(work_space=space)
    except ObjectDoesNotExist:
        return None
