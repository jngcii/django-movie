from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import Movie, Tag, Seho, Favor
from reviews.forms import ReviewForm
# Paginator
from django.core.paginator import Paginator


# use static json
from django.contrib.staticfiles.storage import staticfiles_storage
import json
from pprint import pprint

def index(request):
    # query 받아오기
    keywords = []
    if request.method == 'POST':
        tmp = dict(request.POST).get('keyword', None)
        if tmp:
            keywords = tmp
    movies = Movie.objects.all()
    for keyword in keywords:
        tags = Tag.objects.filter(name=keyword)
        movies = movies.filter(Q(title__icontains=keyword) | Q(original_title__icontains=keyword) | Q(overview__icontains=keyword))
    # paginator
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'movies': movies,
        'page_obj':page_obj,
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
            for tag in movie.tags.all():
                favor = Favor.objects.get(creator=user, tag=tag)
                favor.cnt -= 1
                favor.save()
            result['is_like'] = False
        else:
            seho.is_like = True
            seho.save()
            for tag in movie.tags.all():
                favor = Favor.objects.get(creator=user, tag=tag)
                favor.cnt += 2
                favor.save()
        like_cnt = movie.sehos.filter(is_like=True).count()
        unlike_cnt = movie.sehos.filter(is_like=False).count()
        result['like_cnt'] = like_cnt
        result['unlike_cnt'] = unlike_cnt
            
    except Seho.DoesNotExist:
        for tag in movie.tags.all():
            if Favor.objects.filter(creator=user, tag=tag).exists():
                favor = Favor.objects.get(creator=user, tag=tag)
                favor.cnt += 1
                favor.save()
            else:
                favor = Favor.create(creator=user, tag=tag, cnt=1)
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
            for tag in movie.tags.all():
                favor = Favor.objects.get(creator=user, tag=tag)
                favor.cnt -= 2
                favor.save()
        else:
            for tag in movie.tags.all():
                favor = Favor.objects.get(creator=user, tag=tag)
                favor.cnt += 1
                favor.save()
            seho.delete()
            result['is_unlike'] = False
        like_cnt = movie.sehos.filter(is_like=True).count()
        unlike_cnt = movie.sehos.filter(is_like=False).count()
        result['like_cnt'] = like_cnt
        result['unlike_cnt'] = unlike_cnt
    except Seho.DoesNotExist:
        for tag in movie.tags.all():
            if Favor.objects.filter(creator=user, tag=tag).exists():
                favor = Favor.objects.get(creator=user, tag=tag)
                favor.cnt -= 1
                favor.save()
            else:
                favor = Favor.create(creator=user, tag=tag, cnt=-1)
        seho = Seho.objects.create(is_like=False, creator=user, movie=movie)
        if not seho: result['is_unlike'] = False
        like_cnt = movie.sehos.filter(is_like=True).count()
        unlike_cnt = movie.sehos.filter(is_like=False).count()
        result['like_cnt'] = like_cnt
        result['unlike_cnt'] = unlike_cnt
    
    return JsonResponse(result)


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
        
        if Movie.objects.filter(title=title, release_date=release_date).exists():
            continue

        # 장르만 잠시 빼고 넣음
        movie_obj = Movie.objects.create(
            title=title, 
            original_title=original_title,
            release_date=release_date,
            adult=adult,
            overview=overview,
            poster=poster_url
        )
    
        # 장르만 ManyToMany 추가
        genres = tmp_movie['genres']    # 숫자로 된 리스트
        for genre_num in genres:
            tmp = hangul_genres[genre_num]  # 스트링
            if Tag.objects.filter(name=tmp).exists():
                tag = Tag.objects.get(name=tmp)
            else:
                tag = Tag.objects.create(name=tmp)
            movie_obj.tags.add(tag)

    return render(request, 'movies/index.html')