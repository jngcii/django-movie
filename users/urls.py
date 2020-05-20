from django.urls import path
from . import veiws

app_name = 'auth'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('sighout/', views.signout, name='signout'),
]