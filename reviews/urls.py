from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('<int:review_id>/', views.detail, name='review_detail'),
]