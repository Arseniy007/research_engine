from django.core.exceptions import ObjectDoesNotExist
from .models import User, PasswordResetCode


def get_user_by_name(first_name: str, last_name: str, email: str) -> bool:
    """Checks if user with given name and email exists"""
    try:
        return User.objects.get(first_name=first_name, last_name=last_name, email=email)
    except ObjectDoesNotExist:
        return None


def get_user_by_username(username: str, email: str) -> bool:
    """Checks if user with given username and email exists"""
    try:
        return User.objects.get(username=username, email=email)
    except ObjectDoesNotExist:
        return None


def get_user_by_reset_code(code: str) -> User | None:
    """Checks if user related to given reset code exists"""
    try:
        return PasswordResetCode.objects.get(code=code).user
    except ObjectDoesNotExist:
        return None
