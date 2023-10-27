from string import ascii_lowercase, ascii_uppercase, digits
from random import SystemRandom

from django.db import IntegrityError
from .models import Invitation


# String with all ascii char options for the generator
POPULATION = ascii_lowercase + ascii_uppercase + digits

# Numbers of characters in invitation code
LENGTH_OF_STRING = 15


def generate_invitation(space):
    '''Generates random invitation code and creates its object'''

    # Make sure invitation texts never repeat
    while True:
        # Generate random string
        invitation_code = "".join([SystemRandom().choice(POPULATION) for _ in range(LENGTH_OF_STRING)])

        try:
            new_invitation = Invitation(code=invitation_code, work_space=space)

        except IntegrityError:
            # Generate new code in case of repetition
            continue

        else:
            new_invitation.save()
            return invitation_code
