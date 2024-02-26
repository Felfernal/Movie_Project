from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Movies(models.Model):
    name = models.CharField(max_length=250, unique=True)
    desc = models.CharField(max_length=1000)
    actors = models.CharField(max_length=750)
    year = models.IntegerField()
    genre = models.CharField(max_length=500)
    youtube_url = models.CharField(max_length=1000)
    img = models.ImageField(upload_to='gallery')
    user_name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def get_url(self):
        return reverse('movie_app:movies_by_genre', args=[str(self.slug)])

    def __str__(self):
        return '{}'.format(self.name)


class Review(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    movie = models.ForeignKey(Movies, models.CASCADE)
    review = models.TextField(max_length=250)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.movie)
