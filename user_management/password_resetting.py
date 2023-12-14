from django.core.mail import send_mail
from django.urls import reverse
from .models import PasswordResetCode, User
from research_engine.settings import EMAIL_HOST_USER
from utils.code_generator import generate_code


def generate_password_reset_code(user: User) -> str:
    """Create unique reset code and create its obj"""
    reset_code = generate_code()
    reset_code_obj = PasswordResetCode(user=user, code=reset_code)
    reset_code_obj.save()
    return reset_code


def get_reset_url(request, reset_code: str):
    """Create full-path password resetting url using given reset code"""
    return request.build_absolute_uri(reverse("user_management:reset_password", args=(reset_code,)))


def send_password_resetting_email(user: User, reset_url: str) -> None:
    """Send user "I-forgot-password" email"""
    # TODO

    subject = "Password Resetting"
    message = f"Hi {user}.\n\nHere is your url: {reset_url}"
    sender = EMAIL_HOST_USER
    recipient = (user.email,)

    return send_mail(subject, message, sender, recipient)
