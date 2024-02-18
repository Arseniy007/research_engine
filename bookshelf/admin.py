from django.contrib import admin
from .models import Article, Book, Chapter, Reference, Source, Webpage


# Register your models here.
admin.site.register(Article)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Reference)
admin.site.register(Source)
admin.site.register(Webpage)
