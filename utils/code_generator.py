from random import SystemRandom
from string import ascii_lowercase, ascii_uppercase, digits


# String with all ascii char options for the generator
POPULATION = ascii_lowercase + ascii_uppercase + digits

# Numbers of characters in invitation code
LENGTH_OF_STRING = 15


def generate_code() -> str:
    """Generate random string using chars and digits"""
    return "".join([SystemRandom().choice(POPULATION) for _ in range(LENGTH_OF_STRING)])
