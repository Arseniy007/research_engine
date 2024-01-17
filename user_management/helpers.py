from django.core.exceptions import ObjectDoesNotExist
from .models import PasswordResetCode, User


def get_users_work_spaces(user: User):
    """Get all work spaces user owns or were invited to"""
    return list(user.work_spaces.all()) + list(user.guest_work_spaces.all())


def get_user_by_name(first_name: str, last_name: str, email: str) -> User | None:
    """Checks if user with given name and email exists"""
    try:
        return User.objects.get(first_name=first_name, last_name=last_name, email=email)
    except ObjectDoesNotExist:
        return None


def get_user_by_username(username: str, email: str) -> User | None:
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
