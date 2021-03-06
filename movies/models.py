from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    """
    genre에 해당하는 모델
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    release_date = models.DateField()
    adult = models.BooleanField()
    overview = models.TextField()
    poster = models.URLField()
    tags = models.ManyToManyField(Tag, blank=True, related_name='movies')

    def __str__(self):
        return '{} : {}'.format(self.title, self.release_date)

    @property
    def good_seho(self):
        return self.sehos.filter(is_like=True).count()
    
    @property
    def bad_seho(self):
        return self.sehos.filter(is_like=False).count()


class Seho(models.Model):
    """
    like or unlike movie
    """
    is_like = models.BooleanField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sehos')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sehos')

class Favor(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favors')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='favors')
    cnt = models.IntegerField(default=0)