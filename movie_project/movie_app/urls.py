from django.urls import path
from . import views

app_name = 'movie_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:c_slug>/', views.index, name='movies_by_genre'),
    path('login/details/', views.login, name='login'),
    path('register/details/', views.register, name='registration'),
    path('detail/<int:movie_id>/', views.detail, name='detail'),
    path('add/movie/', views.add, name='add'),
    path('logout', views.logout, name='logout'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('<int:id>/', views.edit, name='edit'),
    path('remove/<int:id>/', views.remove, name='remove'),
    path('edit_review/<int:id>/', views.edit_review, name='edit_review'),
    path('profile/view/', views.profilePage, name='profile'),
    path('editprofile/details/', views.edit_profile, name='editprofile'),
    path('filter/genre/<int:id>', views.genfilter, name='filter'),

]
