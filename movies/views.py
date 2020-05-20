from django.shortcuts import render, get_object_or_404
from django.db.models import Q
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


# def good_seho(request, movie_id):
#     movie = get_object_or_404(Movie, id=movie_id)
#     user = request.user
#     try:
#         seho = Seho.objects.get(creator=user, movie=movie)
#         if seho.is_like:
#             # status = 400
#         else:
#             seho.is_like = True
#             # status = 200
#     except Seho.DoesNotExist:
#         seho = Seho.objects.create(is_like=True, creator=user, movie=movie)
#         if seho:
#             # status = 200
#         else:
#             # status = 400


# def bad_seho(request, movie_id):
#     movie = get_object_or_404(Movie, id=movie_id)
#     user = request.user
#     try:
#         seho = Seho.objects.get(creator=user, movie=movie)
#         if seho.is_like:
#             seho.is_like = False
#             # status = 200
#         else:
#             # status = 400
#     except Seho.DoesNotExist:
#         seho = Seho.objects.create(is_like=False, creator=user, movie=movie)
#         if seho:
#             # status = 200
#         else:
#             # status = 400


# def fetch_movies(request):

#     for movie in movies_api:
#         movie.title

#         for g in movie.genre:
#             for sample in samples:
#                 if sample.id == g:
#                     tmp = sample.name
#                     # Tag.objects.filter(name=tmp).exist()
#                     try:
#                         tag = Tag.objects.get(name=tmp)
#                     except Tag.DoesNotExist:
#                         tag = Tag.objects.create(name=tmp)
#                     movie = Movie.objects.create(title, ori)
#                     movie.tags.add(tag)
                
#     title = models.CharField(max_length=255)
#     original_title = models.CharField(max_length=255)
#     release_date = models.DateField()
#     adult = models.BooleanField()
#     overview = models.TextField()
#     poster = models.URLField()
#     tags = models.ManyToManyField(Tag, blank=True, related_name='movies')
#     genre = [1, 2, 3]