from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm
from .models import Review
from movies.models import Movie

# Create your views here.

@login_required
def review_api(request, id):
    if request.method == 'POST':
        """
        create review
        """
        movie = get_object_or_404(Movie, id=id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.creator = request.user
            review.movie = movie
            review.save()
            return redirect('movies:detail', movie_id)
        else:
            messages.error(request, '리뷰를 다시 입력해주세요')
        return redirect('movies:detail', movie_id)
    

    elif request.method == 'PUT':
        """
        update review
        """
        review = get_object_or_404(Review, id=review_id)
        movie_id = review.movie.id

        if request.user == review.creator:
            if request.method=='POST':
                form = ReviewForm(request, instance=review)
                if form.is_valid():
                    form.save()
                    return redirect('reviews:detail', review_id)
        else:
            messages.error(request, '수정 권한이 없습니다.')
        return redirect('reviews:detail', review_id)
    
    
    elif request.method == 'DELETE':
        """
        delete review
        """
        review = get_object_or_404(Review, id=review_id)
        movie_id = review.movie.id
        if request.user == review.creator:
            review.delete()
            return redirect('movies:detail', movie_id)
        else:
            messages.error(request, '삭제 권한이 없습니다.')
        return redircet('reviews:detail', review_id)
