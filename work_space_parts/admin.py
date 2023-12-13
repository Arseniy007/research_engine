from django.contrib import admin
from .models import Comment, Link, Note

# Register your models here.
admin.site.register(Comment)
admin.site.register(Link)
admin.site.register(Note)
