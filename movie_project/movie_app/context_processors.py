from .models import Genre


def genre_names(request):
    gennames = Genre.objects.all()
    return dict(gennames=gennames)
