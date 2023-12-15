from django.contrib import admin
from .models import PasswordResetCode, User


# Register your models here.
admin.site.register(PasswordResetCode)
admin.site.register(User)
