from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import Movie, Tag, Seho
from reviews.forms import ReviewForm


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
    form = ReviewForm()

    context = {
        'movie': movie,
        'form': form,
    }

    return render(request, 'movies/detail.html', context)


def good_seho(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user
    result = {
        'is_like': True,
        'is_unlike': False,
        'like_cnt': 0,
        'unlike_cnt': 0
    }
    try:
        seho = Seho.objects.get(creator=user, movie=movie)
        if seho.is_like:
            seho.delete()
            result['is_like'] = False
        else:
            seho.is_like = True
            seho.save()
        like_cnt = movie.sehos.filter(is_like=True).count()
        unlike_cnt = movie.sehos.filter(is_like=False).count()
        result['like_cnt'] = like_cnt
        result['unlike_cnt'] = unlike_cnt
            
    except Seho.DoesNotExist:
        seho = Seho.objects.create(is_like=True, creator=user, movie=movie)
        if not seho: result['is_like'] = False
        like_cnt = movie.sehos.filter(is_like=True).count()
        unlike_cnt = movie.sehos.filter(is_like=False).count()
        result['like_cnt'] = like_cnt
        result['unlike_cnt'] = unlike_cnt
    
    return JsonResponse(result)


def bad_seho(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user
    result = {
        'is_like': False,
        'is_unlike': True,
        'like_cnt': 0,
        'unlike_cnt': 0
    }
    try:
        seho = Seho.objects.get(creator=user, movie=movie)
        if seho.is_like:
            seho.is_like = False
            seho.save()
        else:
            seho.delete()
            result['is_unlike'] = False
        like_cnt = movie.sehos.filter(is_like=True).count()
        unlike_cnt = movie.sehos.filter(is_like=False).count()
        result['like_cnt'] = like_cnt
        result['unlike_cnt'] = unlike_cnt
    except Seho.DoesNotExist:
        seho = Seho.objects.create(is_like=False, creator=user, movie=movie)
        if not seho: result['is_unlike'] = False
        like_cnt = movie.sehos.filter(is_like=True).count()
        unlike_cnt = movie.sehos.filter(is_like=False).count()
        result['like_cnt'] = like_cnt
        result['unlike_cnt'] = unlike_cnt
    
    return JsonResponse(result)


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