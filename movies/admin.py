from django.contrib import admin
from .models import Movie, Tag
# Register your models here.

admin.site.register(Movie)
admin.site.register(Tag)