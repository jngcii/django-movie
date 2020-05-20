from django.shortcuts import render, get_object_or_404
from django.db.models imoprt Q
from .models import Movie, Tag


def index(request):
    # query 받아오기
    keywords = []
    movies = Movie.objects.all()
    for keyword in keywords:
        tags = Tag.objects.filter(name=keyword)
        movies = movie.filter(Q(title__icontains=keyword) | Q(tags__in=tags))
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


def detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    context = {
        'movie': movie
    }

    return render(request, 'movies/detail.html', context)
