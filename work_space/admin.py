from django.contrib import admin
from .models import Invitation, ShareSpaceCode, WorkSpace

# Register your models here.
admin.site.register(Invitation)
admin.site.register(ShareSpaceCode)
admin.site.register(WorkSpace)
