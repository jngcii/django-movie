from django.shortcuts import render, get_object_or_404
from django.db.models imoprt Q
from .models import Movie, Tag, Seho


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


def good_seho(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user
    try:
        seho = Seho.objects.get(creator=user, movie=movie)
        if seho.is_like:
            # status = 400
        else:
            seho.is_like = True
            # status = 200
    except Seho.DoesNotExist:
        seho = Seho.objects.create(is_like=True, creator=user, movie=movie)
        if seho:
            # status = 200
        else:
            # status = 400


def bad_seho(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user
    try:
        seho = Seho.objects.get(creator=user, movie=movie)
        if seho.is_like:
            seho.is_like = False
            # status = 200
        else:
            # status = 400
    except Seho.DoesNotExist:
        seho = Seho.objects.create(is_like=False, creator=user, movie=movie)
        if seho:
            # status = 200
        else:
            # status = 400
