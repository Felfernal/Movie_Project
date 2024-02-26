from django import forms
from django.contrib.auth.models import User

from .models import Movies, Review


class Movie_Form(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['name', 'desc', 'actors', 'year', 'genre', 'youtube_url', 'img']


class Review_Form(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'rating']


class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']