from django.db import models
from movies.models import Movie
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)