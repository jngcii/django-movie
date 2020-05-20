from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Movie, Tag, Seho
# use static json
from django.contrib.staticfiles.storage import staticfiles_storage
import requests
import json

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


def fetch_movies(request):
    json_path = staticfiles_storage.path('movies/moviedata.json')
    # print('json_path:', json_path)
    
    with open(json_path) as json_file:
        json_data = json.load(json_file)

    # 0~18=> 장르 / 19~ 영화
    genre_data = json_data[:19]
    movie_data = json_data[19:]
    
    # 장르 딕셔너리 생성 & tag생성
    hangul_genres = {
        12: '모험',
        14: '판타지',
        16: '애니메이션',
        18: '드라마',
        27: '호러',
        28: '액션',
        35: '코미디',
        36: '사극',
        37: '서부극',
        53: '스릴러',
        80: '범죄',
        99: '다큐멘터리',
        878: '공상과학',
        9648: '미스터리',
        10402: '뮤지컬',
        10749: '로맨스',
        10751: '가족',
        10752: '전쟁',
        10770: 'TV영화'}
    
    # 장르(였던것)
    
    for genre_name in hangul_genres.values():        
        tag = Tag.objects.create(name=genre_name)

    # movie 오브젝트 생성
    for movie_json in movie_data:
        tmp_movie = movie_json['fields']
        title = tmp_movie['title']
        original_title = tmp_movie['original_title']
        release_date = tmp_movie['release_date']
        adult = tmp_movie['adult']
        overview = tmp_movie['overview']
        poster = tmp_movie['poster_path']
        poster_url = 'https://image.tmdb.org/t/p/w780/' + poster
        
        # 장르만 잠시 빼고 넣음
        movie_obj = Movie.objects.create(
            title=title, 
            original_title=original_title,
            release_date=release_date,
            adult=adult,
            overview=overview,
            poster=poster_url)
    
        # 장르만 ManyToMany 추가
        genres = tmp_movie['genres']
        for genre_num in genres:
            tmp = hangul_genres[genre_num]
            try:
                tag = Tag.objects.get(name=tmp)
            except:
                tag = Tag.objects.create(name=tmp)

            movie_obj.tags.add(tag)
        return render(request, 'movies/index.html')