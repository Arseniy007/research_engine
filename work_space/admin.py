from django.contrib import admin
from .models import Comment, Invitation, ShareSpaceCode, WorkSpace

# Register your models here.
admin.site.register(Comment)
admin.site.register(Invitation)
admin.site.register(ShareSpaceCode)
admin.site.register(WorkSpace)
