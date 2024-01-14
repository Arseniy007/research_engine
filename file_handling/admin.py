from django.contrib import admin
from .models import PaperFile, SourceFile


# Register your models here.
admin.site.register(PaperFile)
admin.site.register(SourceFile)
