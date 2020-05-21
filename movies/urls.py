from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('<int:movie_id>/', views.detail, name='detail'),
    path('<int:movie_id>/good/', views.good_seho, name='good'),
    path('<int:movie_id>/bad/', views.bad_seho, name='bad'),
    path('fetch_movies/', views.fetch_movies, name='fetch_movies'),
    path('get_favors/', views.get_favor_movies, name='get_favor_movies'),
]