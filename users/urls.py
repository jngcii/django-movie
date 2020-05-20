from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('join/', views.signup, name='signup'),
    path('login/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
]