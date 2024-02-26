from django.contrib import admin
from .models import Movies, Genre, Review


# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'actors', 'year', 'genre', 'youtube_url', 'img']


admin.site.register(Movies)


class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Genre, GenreAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'movie', 'rating', 'created_at']
    readonly_fields = ['created_at', ]


admin.site.register(Review, ReviewAdmin)
