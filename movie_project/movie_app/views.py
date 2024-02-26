from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Movies, Review, Genre
from .forms import Movie_Form, Review_Form, User_Form
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def homePage(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        username1 = request.POST['Username']
        password1 = request.POST['pwd']
        user = auth.authenticate(username=username1, password=password1)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Username or Password is incorrect")
            return render(request, 'login.html')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def update(request, id):
    movie = Movies.objects.get(id=id)
    form = Movie_Form(request.POST or None, request.FILES, instance=movie)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'edit.html', {'form': form, 'movie': movie})


def edit_review(request, id):
    review = Review.objects.get(id=id)
    movie_name = review.movie
    movie = Movies.objects.get(name=movie_name)
    form = Review_Form(request.POST or None, request.FILES, instance=review)
    if form.is_valid():
        form.save()
        review = Review.objects.filter(movie=movie)
        return render(request, "detail.html", {'movie': movie, 'review': review})
    return render(request, 'edit_review.html', {'form': form, 'review': review})


def profilePage(request):
    return render(request, 'profile.html')


def delete(request, id):
    if request.method == 'POST':
        movie = Movies.objects.get(id=id)
        movie.delete()
        return redirect('/')
    return render(request, 'delete.html')


def index(request, c_slug=None):
    movie = Movies.objects.all()
    c_page = None
    movie_list = None
    if c_slug is not None:
        c_page = get_object_or_404(Genre, slug=c_slug)
        movie_list = Movies.objects.all().filter(genre=c_page, name=True)
    else:
        movie_list = Movies.objects.all().filter(name=True)
    paginator = Paginator(movie_list, 16)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        movies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        movies = paginator.page(paginator.num_pages)

    return render(request, "index.html", {'genre': c_page, 'movies': movies, 'movie_list': movie})


def detail(request, movie_id):
    movie = Movies.objects.get(id=movie_id)
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        mov_id = movie_id
        movie = Movies.objects.get(id=movie_id)
        review1 = request.POST.get('review')
        review1.capitalize()
        rating = request.POST.get('rating')
        user = request.user
        if review1 != "":
            if rating is not None:
                Review(user=user, movie=movie, review=review1, rating=rating).save()
                review = Review.objects.filter(movie=movie)
                return render(request, "detail.html", {'movie': movie, 'review': review})
            else:
                messages.info(request,
                              "Please select rating before submitting!")
                review = Review.objects.filter(movie=movie)
                return render(request, 'detail.html', {'movie': movie, 'review': review})
        else:
            messages.info(request,
                          "Review cannot be blank before submitting!")
            review = Review.objects.filter(movie=movie)
            return render(request, "detail.html", {'movie': movie, 'review': review})
    review = Review.objects.filter(movie=movie)
    return render(request, "detail.html", {'movie': movie, 'review': review})


def genfilter(request, id):
    genre = Genre.objects.get(id=id)
    movies = Movies.objects.all()
    return render(request, 'filter.html', {'genre': genre, 'movies': movies})


def register(request):
    if request.method == 'POST':
        usernm = request.POST['Username']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        mail = request.POST['mail']
        password = request.POST['pwd']
        password1 = request.POST['pwd1']
        if usernm != "":
            if fname != "":
                if lname != "":
                    if mail != "":
                        if password != "":
                            if password1 != "":
                                if password == password1:
                                    if User.objects.filter(username=usernm).exists():
                                        messages.info(request,
                                                      "Username already in use. Please select a different one.")
                                        return render(request, 'register.html')
                                    elif User.objects.filter(email=mail).exists():
                                        messages.info(request, "This mail is already registered.")
                                        return render(request, 'register.html')
                                    else:
                                        user = User.objects.create_user(username=usernm, password=password,
                                                                        first_name=fname, last_name=lname,
                                                                        email=mail)
                                        user.save()

                                        messages.info(request, "Welcome to Moovys")
                                        return render(request, 'login.html')

                                else:
                                    messages.info(request, "Passwords don't match")
                                    return render(request, 'register.html')
                            else:
                                messages.info(request, "Confirm Password cannot be empty!")
                                return render(request, 'register.html')
                        else:
                            messages.info(request, "Password cannot be empty!")
                            return render(request, 'register.html')
                    else:
                        messages.info(request, "E-mail cannot be empty!")
                        return render(request, 'register.html')
                else:
                    messages.info(request, "Please enter your last name!")
                    return render(request, 'register.html')
            else:
                messages.info(request, "Please enter your first name!")
                return render(request, 'register.html')
        else:
            messages.info(request, "Username cannot be empty!")
            return render(request, 'register.html')

    return render(request, 'register.html')


def add(request):
    if request.method == 'POST':
        usr_name = request.user.username
        mov_name = request.POST.get('name')
        mov_desc = request.POST.get('desc')
        mov_year = request.POST.get('year')
        mov_actors = request.POST.get('actors')
        mov_genre = request.POST.getlist('genre')
        mov_img = request.FILES['img']
        mov_url = request.POST.get("youtube_url")
        movie = Movies(name=mov_name, desc=mov_desc, year=mov_year, actors=mov_actors, genre=mov_genre, img=mov_img,
                       youtube_url=mov_url, user_name=usr_name)
        movie.save()
        return redirect('/')
    return render(request, 'add.html')


def allMovieGenre(request):
    return redirect(request, 'home.html')


def edit_profile(request):
    form = User_Form(data=request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'edit_profile.html', {'form': form})


def edit(request, id):
    rev = Review.objects.get(id=id)
    movie_name = rev.movie
    movie = Movies.objects.get(name=movie_name)
    form = Review_Form(request.POST or None, request.FILES, instance=rev)
    if form.is_valid():
        form.save()
        return render(request, 'detail.html', {'movie': movie})
    return render(request, 'edit.html', {'form': form, 'movie': movie})


def remove(request, id):
    if request.method == 'POST':
        rev = Review.objects.get(id=id)
        movie_name = rev.movie
        movie = Movies.objects.get(name=movie_name)
        rev.delete()
        review = Review.objects.filter(movie=movie)
        return render(request, "detail.html", {'movie': movie, 'review': review})
    return render(request, 'remove.html')
