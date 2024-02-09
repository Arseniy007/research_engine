from django.contrib import admin
from .models import Invitation, ShareSourcesCode, WorkSpace

# Register your models here.
admin.site.register(Invitation)
admin.site.register(ShareSourcesCode)
admin.site.register(WorkSpace)
