from django.contrib import admin

from .models import WorkSpace, Invitation, Comment

# Register your models here.
admin.site.register(WorkSpace)
admin.site.register(Invitation)
admin.site.register(Comment)

