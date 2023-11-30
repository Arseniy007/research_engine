from random import SystemRandom
from string import ascii_lowercase, ascii_uppercase, digits
from django.db import IntegrityError
from .models import Invitation, ShareSpaceCode, WorkSpace


# String with all ascii char options for the generator
POPULATION = ascii_lowercase + ascii_uppercase + digits

# Numbers of characters in invitation code
LENGTH_OF_STRING = 15


def generate_invitation(space: WorkSpace, invite=False) -> str:
    """Generates random invitation code and creates its object"""
    
    # Make sure invitation texts never repeat
    while True:
        # Generate random string
        invitation_code = "".join([SystemRandom().choice(POPULATION) for _ in range(LENGTH_OF_STRING)])
        try:
            if invite:
                code_obj = Invitation(code=invitation_code, work_space=space)
            else:
                code_obj = ShareSpaceCode(code=invitation_code, work_space=space)
        except IntegrityError:
            # Generate new code in case of repetition
            continue
        else:
            code_obj.save()
            return invitation_code
