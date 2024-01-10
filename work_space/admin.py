from django.contrib import admin
from .models import Invitation, Link, ShareSourcesCode, WorkSpace

# Register your models here.
admin.site.register(Invitation)
admin.site.register(Link)
admin.site.register(ShareSourcesCode)
admin.site.register(WorkSpace)
