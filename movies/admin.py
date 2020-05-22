from django.contrib import admin
from .models import Movie, Seho, Tag

# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'adult',]

admin.site.register(Movie, MovieAdmin)
admin.site.register(Seho)
admin.site.register(Tag)