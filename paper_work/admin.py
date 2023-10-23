from django.contrib import admin
from .models import Paper, PaperVersion

# Register your models here.
admin.site.register(Paper)
admin.site.register(PaperVersion)
