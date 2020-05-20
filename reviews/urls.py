from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('<int:id>/', views.review_api, name='review_api'),
]